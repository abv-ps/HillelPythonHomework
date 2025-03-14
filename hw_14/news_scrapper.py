"""
This module is designed to scrape news articles from a given news website,
process the data, and save it to a CSV file.

It provides functionality to fetch web pages, extract relevant information
from news articles, and perform filtering based on specified date ranges.

The module uses asynchronous requests to scrape the news articles
concurrently for improved performance.

Functions included in the module:
1. `get_page`: Fetches a web page and returns a BeautifulSoup object.
2. `convert_date`: Converts a date from Ukrainian format
   to a standardized format (YYYY-MM-DD HH:MM).
3. `is_news_page`: Checks if a URL corresponds to a news article page.
4. `fetch_news_details`: Fetches details (date and summary)
   of a news article asynchronously.
5. `parse_news`: Parses a news page and returns a list of news articles,
   filtered by date if provided.
6. `save_to_csv`: Saves the scraped news data to a CSV file.
7. `generate_news_statistics`: Generates statistics about the scraped news articles
   and displays them as a bar chart.
8. `main`: Orchestrates the entire scraping process, fetches news from multiple pages,
   and saves the results.
"""
import csv
import asyncio
import aiohttp
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Tuple, Any
from config import Config

import requests
from bs4 import BeautifulSoup, Tag, FeatureNotFound
import pandas as pd
import matplotlib.pyplot as plt

from validate_filtration import UserInputValidator
from logger_config import get_logger
from error_handler import handle_action_error, handle_file_error

logger = get_logger(__name__, "news_scraper.log")


def get_page(url: str) -> Optional[BeautifulSoup]:
    """
    Fetches a web page and returns a BeautifulSoup object.

    Args:
        url (str): The URL to fetch.

    Returns:
        Optional[BeautifulSoup]: A BeautifulSoup object if the request is successful,
                                 otherwise None.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        error_message = handle_action_error(url, "fetching", e)
        logger.error(error_message)
        return None


def convert_date(input_string: str) -> str:
    """
    Converts a date from Ukrainian format to a standardized format.

    Args:
        input_string (str): The input date string in Ukrainian format.

    Returns:
        str: A formatted date string in 'YYYY-MM-DD HH:MM' format.
    """
    formatted_date = re.search(r'(\d{1,2} \w+ \d{4} \d{2}:\d{2})', input_string)
    if formatted_date:
        input_string = formatted_date.group(1)
        month_translation = {
            "січня": "January", "лютого": "February", "березня": "March",
            "квітня": "April", "травня": "May", "червня": "June",
            "липня": "July", "серпня": "August", "вересня": "September",
            "жовтня": "October", "листопада": "November", "грудня": "December"
        }
        for ukr_month, eng_month in month_translation.items():
            if ukr_month in input_string:
                input_string = input_string.replace(ukr_month, eng_month)
        datetime_object = datetime.strptime(input_string, "%d %B %Y %H:%M")
        return datetime_object.strftime('%Y-%m-%d %H:%M')
    return ""


def is_news_page(url: str) -> bool:
    """
    Checks if the given URL corresponds to a news page.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL does not contain only numbers after 'news/',
              otherwise False.
    """
    return not bool(re.search(r'/news(?:/\d+)?$', url))


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Parses a date string in the format 'YYYY-MM-DD' and returns a date object.

    Args:
        date_str (Optional[str]): The date string to parse.

    Returns:
        Optional[datetime]: A datetime object if parsing is successful, otherwise None.
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def is_within_date_range(news_date: Optional[datetime], start_date: Optional[str],
                         end_date: Optional[str]) -> bool:
    """
    Checks if a given date is within the specified date range.

    Args:
        news_date (Optional[datetime]): The date of the news article.
        start_date (Optional[str]): The start date as a string ('YYYY-MM-DD') or None.
        end_date (Optional[str]): The end date as a string ('YYYY-MM-DD') or None.

    Returns:
        bool: True if the news date is within range, False otherwise.
    """
    if not news_date:
        return False

    start = parse_date(start_date)
    end = parse_date(end_date)

    if start and news_date < start:
        return False
    if end and news_date >= end:
        return False

    return True


async def fetch_news_details(session: aiohttp.ClientSession, link: str) -> Dict[str, Optional[str]]:
    """
    Fetches details of a news article asynchronously.

    Args:
        session (aiohttp.ClientSession): The aiohttp session object.
        link (str): The URL of the news article.

    Returns:
        Dict[str, Optional[str]]: A dictionary containing the date and summary
                                   of the news article.
    """
    try:
        async with session.get(link) as response:
            response.raise_for_status()

            html = await response.text()

            try:
                soup = BeautifulSoup(html, 'html.parser')
            except FeatureNotFound as bs_err:
                error_message = handle_action_error(link, "parsing HTML", error=bs_err)
                logger.error(error_message)
                return {'date': None, 'summary': None}

            time_tag = soup.find('div', class_=re.compile("time"))
            date = convert_date(time_tag.get_text(strip=True)) if time_tag else datetime.now().strftime(
                '%Y-%m-%d %H:%M')

            summary_tag = soup.find('div', class_='publication-lead')
            summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

            return {'date': date, 'summary': summary}
    except aiohttp.ClientResponseError as http_err:
        error_message = handle_action_error(link, "fetching news details",
                                            error=http_err, status_code=http_err.status)
        logger.error(error_message)
    except aiohttp.ClientError as http_err:
        error_message = handle_action_error(link, "fetching news details", error=http_err)
        logger.error(error_message)
    except Exception as e:
        error_message = handle_action_error(link, "fetching news details", error=e)
        logger.error(error_message)

    return {'date': None, 'summary': None}


async def parse_news(url: str, date_filter: Tuple[Optional[str], Optional[str]]) -> (
        List)[Dict[str, str]]:
    """
    Parses news articles from a given URL.

    Args:
        url (str): The URL of the news page.
        date_filter (Tuple[Optional[str], Optional[str]]): A tuple containing the start
                                                           and end date for filtering.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing news details.
    """
    news_list: List[Dict[str, str]] = []
    soup = get_page(url)
    if not soup:
        return news_list

    news_items = extract_news_items(soup, url)
    if not news_items:
        return news_list

    news_details = await fetch_news_details_batch(news_items)
    return process_news_items(news_items, news_details, date_filter)


def extract_news_items(soup: BeautifulSoup, url: str) -> List[Tag]:
    """
    Extracts news items from the parsed HTML.

    Args:
        soup (BeautifulSoup): The parsed HTML document.
        url (str): The URL from which the HTML was fetched.

    Returns:
        List[Tag]: A list of 'a' tags representing news items,
                    or an empty list if no newsline is found.
    """
    newsline = soup.find('div', class_='newsline')
    if not newsline:
        logger.warning("No newsline found on %s", url)
        return []
    return newsline.find_all('a')


async def fetch_news_details_batch(news_items: List[Tag]) -> List[Dict[str, Any]]:
    """
    Fetches details for all news items asynchronously.

    Args:
        news_items (List[Tag]): A list of tags representing news items.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing news details
                               for each item, such as title, summary, and date.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_news_details(session, href)
            for item in news_items
            if (href := item.get('href')) and isinstance(href, str) and is_news_page(href)
        ]
        return await asyncio.gather(*tasks)


def process_news_items(news_items: List[Tag], news_details: List[Dict[str, Any]],
                       date_filter: Tuple[Optional[str], Optional[str]]) -> List[Dict[str, str]]:
    """
    Processes news items, filters by date, and formats output.

    Args:
        news_items (List[Tag]): A list of 'a' tags representing news items.
        news_details (List[Dict[str, Any]]): A list of dictionaries containing the details
                                              of each news item.
        date_filter (Tuple[Optional[str], Optional[str]]): A tuple containing the start and
                                                            end date for filtering news.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing filtered and formatted
                               news information including title, link, date, and summary.
    """
    news_list = []
    for item, details in zip(news_items, news_details):
        title = re.sub(r"^\d{2}:\d{2}\s*", "", item.get_text(strip=True))
        link = clean_string(item.get('href', ''))
        news_date_str = str(details.get('date', ''))
        news_date = parse_date(news_date_str.split(' ')[0] if news_date_str else "")

        if not is_within_date_range(news_date, *date_filter):
            continue

        summary = clean_string(details.get('summary', ''))
        news_list.append({
            'title': title,
            'link': link,
            'date_with_time': news_date_str,
            'summary': summary,
        })
        logger.info("News details for news article %s: %s", title, news_date)

    return news_list


def clean_string(value: Any) -> str:
    """
    Cleans and ensures that the input value is a valid string.

    If the input is a string, it is stripped of leading and trailing whitespace.
    If the input is a list, each element is stripped and then joined into a single string.
    If the input is neither a string nor a list, an empty string is returned.

    Args:
        value (Any): The input value to be cleaned,
        which can be a string or a list of strings.

    Returns:
        str: A cleaned string, either from the input string or a concatenated string
             from the list, or an empty string if the input is neither.
    """
    if isinstance(value, str):
        return value.strip()
    elif isinstance(value, list):
        return " ".join(map(str.strip, value))
    else:
        return ""


def save_to_csv(data: List[Dict[str, str]], filename: str = 'news.csv') -> None:
    """
    Saves the news data to a CSV file.

    Args:
        data (List[Dict[str, str]]): List of dictionaries containing news details.
        filename (str): Name of the CSV file where data will be saved.

    Returns:
        None
    """
    if not data:
        logger.warning("No news data to save.")
        return

    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'link', 'date_with_time', 'summary'])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(data)
        logger.info("News saved to %s.", filename)
    except Exception as e:
        error_message = handle_file_error('write', filename, e)
        logger.error(error_message)


def get_next_plot_filename(directory: Path) -> Path:
    """
    Finds the next available filename for saving a plot in the given directory.

    This function looks for existing PNG files in the specified directory,
    extracts the numeric part of their filenames, and returns the next available
    filename by incrementing the highest number found.

    Args:
        directory (Path): The directory where the plot will be saved.

    Returns:
        Path: The next available filename as a Path object.
    """
    directory.mkdir(parents=True, exist_ok=True)

    existing_files = {
        int(p.stem.split(", ")[1])
        for p in directory.glob("plot, *.png")
        if p.stem.split(", ")[1].isdigit()
    }

    next_index = max(existing_files, default=0) + 1

    return directory / f"plot, {next_index}.png"


def generate_news_statistics(news_list: List[Dict[str, str]],
                             save_path: Optional[Path] = None) -> None:
    """
    Generates and displays statistics about the collected news articles.

    Args:
        news_list (List[Dict[str, str]]): List of dictionaries containing news details.
        save_path (Optional[Path]): Path to save the plot instead of displaying it.

    Returns:
        None
    """
    df = pd.DataFrame(news_list)

    if df.empty:
        logger.warning("DataFrame is empty. No statistics to generate.")
        return

    if 'date_with_time' not in df.columns:
        logger.error("Missing 'date_with_time' column in DataFrame.")
        logger.error("Available columns: %s", list(df.columns))
        return

    df['date_with_time'] = pd.to_datetime(df['date_with_time'], format='%Y-%m-%d %H:%M', errors='coerce')
    df['date'] = df['date_with_time'].dt.date

    if df['date'].isna().all():
        logger.error("Failed to extract date from 'date_with_time'.")
        return

    stats = df.groupby('date').size().reset_index(name='count')

    print("News statistics by date:")
    print(stats)

    ax = stats.plot(x='date', y='count', kind='bar', title='News Count by Date', legend=False)

    for i, v in enumerate(stats['count']):
        ax.text(i, v + 0.1, str(v), ha='center', va='bottom')

    plt.xticks(rotation=35, ha='right', fontsize=7)

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight')
        logger.info("Plot saved to %s", save_path)
    else:
        plt.show()

    plt.close()


async def main() -> None:
    """
    Main function that orchestrates the news scraping process.

    Returns:
        None
    """
    all_news: List[Dict[str, str]] = []
    validator = UserInputValidator()
    date_filter = await validator.select_filter_mode()

    for page in range(Config.PAGE_RANGE[0], Config.PAGE_RANGE[1]):
        url = Config.BASE_URL.format(page=page)
        news_data = await parse_news(url, date_filter)
        all_news.extend(news_data)

    save_to_csv(all_news)
    plot_path = get_next_plot_filename(Path(Config.PLOT_DIR))
    generate_news_statistics(all_news, save_path=plot_path)


if __name__ == '__main__':
    asyncio.run(main())
