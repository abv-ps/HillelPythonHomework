import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from logger_config import get_logger
from typing import Optional, TextIO
from error_handler import handle_action_error, handle_file_error

logger = get_logger(__name__, "news_scrapper.log")

def get_page(url: str) -> Optional[BeautifulSoup]:
    """
    Downloads the HTML code of the given URL and returns a BeautifulSoup object.

    Args:
        url: The URL of the page to download.

    Returns:
        A BeautifulSoup object representing the parsed HTML or None if error occurred.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        error_message = handle_action_error(url, "fetching", e)
        logger.error(error_message)
        return None


def parse_news(soup: Optional[BeautifulSoup]) -> list[dict]:
    """
    Extracts news from the given BeautifulSoup object.

    Args:
        soup: The BeautifulSoup object containing the parsed HTML.

    Returns:
        A list of dictionaries containing news details (title, link, date, summary).
    """
    news_list = []
    if not soup:
        return news_list

    news_items = soup.select('.im-tl a')  # Selecting news links
    logger.info("Starting to add information...")
    for item in news_items:
        title = item.get_text(strip=True)
        link = item['href'] if item.has_attr('href') else ''
        date = datetime.now().strftime('%Y-%m-%d')  # Assuming news is from today
        logger.info("Link: %s; Title: %s; Date: %s", link, title, datetime)
        summary = ''  # Ukr.net does not provide summaries on the main page
        news_list.append({
            'title': title,
            'link': link,
            'date': date,
            'summary': summary
        })
    logger.info("Information has been added...")
    return news_list


def save_to_csv(data: list[dict], filename: str = 'news.csv') -> None:
    """
    Saves the list of news articles to a CSV file.

    Args:
        data: A list of dictionaries containing news details.
        filename: The name of the CSV file.
    """
    if not data:
        logger.warning("No news data to save.")
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'link', 'date', 'summary'])
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"News saved to {filename}")
    except Exception as e:
        error_message = handle_file_error('write', filename, e)
        logger.error(error_message)


if __name__ == '__main__':
    URL = "https://www.ukr.net/news/main.html"
    soup = get_page(URL)
    if soup:
        news_data = parse_news(soup)
        save_to_csv(news_data)
