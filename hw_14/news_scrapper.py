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
import re
import asyncio
from datetime import datetime, date
from typing import Optional, List, Dict, Tuple

import requests
import aiohttp
from bs4 import BeautifulSoup, Tag
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
        url: The URL to fetch.

    Returns:
        A BeautifulSoup object if the request is successful, otherwise None.
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
        input_string: The input date string in Ukrainian format.

    Returns:
        A formatted date string in 'YYYY-MM-DD HH:MM' format.
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
        url: The URL to check.

    Returns:
        True if the URL does not contain only numbers after 'news/', otherwise False.
    """
    return not bool(re.search(r'/news/(\d+)$', url))


async def fetch_news_details(session: aiohttp.ClientSession, link: str) -> (
        Dict)[Optional[str], Optional[str]]:
    """
    Fetches details of a news article asynchronously.

    Args:
        session: The aiohttp session object.
        link: The URL of the news article.

    Returns:
        A dictionary containing the date and summary of the news article.
    """
    try:
        async with session.get(link) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            time_tag = soup.find('div', class_=re.compile("time"))
            if time_tag:
                date = convert_date(time_tag.get_text(strip=True))
            else:
                date = datetime.now().strftime('%Y-%m-%d %H:%M')
            summary_tag = soup.find('div', class_='publication-lead')
            summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"
            return {'date': date, 'summary': summary}
    except Exception as e:
        logger.error("Error fetching details for %s: %s", link, e)
        return {'date': None, 'summary': None}


async def parse_news(url: str, date_filter: Tuple[Optional[str], Optional[str]]) -> (
        List)[Dict[str, str]]:
    """
    Parses news articles from a given URL.

    Args:
        url: The URL of the news page.
        date_filter: A tuple containing the start and end date for filtering.

    Returns:
        A list of dictionaries containing news details.
    """
    news_list: List[Dict[str, str]] = []
    soup = get_page(url)
    if not soup:
        return news_list
    newsline = soup.find('div', class_='newsline')
    if not newsline:
        logger.warning("No newsline found on %s", url)
        return news_list
    news_items: List[Tag] = []
    if isinstance(newsline, Tag):
        news_items = newsline.find_all('a')
    logger.info("Found %s news items on %s. "
                "Starting to fetch details...", len(news_items), url )
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_news_details(session, href) for href in (item.get('href') for item in news_items)
            if href and isinstance(href, str) and is_news_page(href)
        ]
        news_details = await asyncio.gather(*tasks)
    for item, details in zip(news_items, news_details):
        title = item.get_text(strip=True)
        link = item.get('href')
        news_date = details['date']
        news_date_without_time = news_date.split(' ')[0] if news_date else ""
        if news_date_without_time:
            news_date_without_time = datetime.strptime(news_date_without_time, "%Y-%m-%d").date()

        start_date, end_date = date_filter
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        logger.info("Date of news is %s %s. "
                    "\nStart date is %s %s. "
                    "\nEnd date is %s %s. ", news_date_without_time,
                    isinstance(news_date_without_time, date),
                    start_date,
                    isinstance(start_date, date),
                    end_date,
                    isinstance(end_date, date))
        if start_date and news_date_without_time <= start_date:
            continue
        if end_date and news_date_without_time > end_date:
            continue
        summary = details['summary']
        if isinstance(summary, list):
            summary = " ".join(summary) if summary else None
        elif not isinstance(summary, str):
            summary = None
        news_list.append({
            'title': str(title) if isinstance(title, str) else '',
            'link': str(link) if isinstance(link, str) else '',
            'date_with_time': news_date or '',
            'summary': summary or '',
        })
        logger.info("News details for news article %s: %s", title, news_date)
    logger.info("Finished fetching news details from %s.", url)
    return news_list


def save_to_csv(data: List[Dict[str, str]], filename: str = 'news.csv') -> None:
    """
    Saves the news data to a CSV file.

    Args:
        data: List of dictionaries containing news details.
        filename: Name of the CSV file where data will be saved.

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
        logger.info("News saved to %s.", filename )
    except Exception as e:
        error_message = handle_file_error('write', filename, e)
        logger.error(error_message)


def generate_news_statistics(news_list: List[Dict[str, str]]) -> None:
    """
    Generates and displays statistics about the collected news articles.

    Args:
        news_list: List of dictionaries containing news details.

    Returns:
        None
    """
    df = pd.DataFrame(news_list)

    if df.empty:
        logger.warning("DataFrame is empty. No statistics to generate.")
        return

    if 'date_with_time' not in df.columns:
        logger.error("Missing 'date_with_time' column in DataFrame.", )
        logger.error("Available columns: %s", df.columns)
        return

    df['date_with_time'] = pd.to_datetime(df['date_with_time'],
                                          format='%Y-%m-%d %H:%M', errors='coerce')
    df['date'] = df['date_with_time'].dt.date

    if df['date'].isna().all():
        logger.error("Failed to extract date from 'date_with_time'.")
        return

    stats = df.groupby('date').size().reset_index(name='count')

    print("News statistics by date:")
    print(stats)

    ax = stats.plot(x='date', y='count', kind='bar', title='News Count by Date')

    for i, v in enumerate(stats['count']):
        ax.text(i, v + 0.1, str(v), ha='center', va='bottom')

    plt.xticks(rotation=35, ha='right', fontsize=7)
    plt.show()


async def main() -> None:
    """
    Main function that orchestrates the news scraping process.

    Returns:
        None
    """
    all_news: List[Dict[str, str]] = []
    validator = UserInputValidator()
    date_filter = validator.select_filter_mode()

    for page in range(1, 3):
        url = f"https://www.rbc.ua/rus/news/{page}"
        news_data = await parse_news(url, date_filter)
        all_news.extend(news_data)

    save_to_csv(all_news)
    generate_news_statistics(all_news)


if __name__ == '__main__':
    asyncio.run(main())
