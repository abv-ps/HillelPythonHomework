import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from logger_config import get_logger
from typing import Optional, List, Dict
from error_handler import handle_action_error, handle_file_error

# Логгер для запису повідомлень
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


def parse_news(soup: Optional[BeautifulSoup]) -> List[Dict[str, str]]:
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

    # Знайдемо всі <article> елементи з атрибутом data-id
    articles = soup.find_all('article', attrs={'data-id': True})

    for article in articles:
        # Витягнемо data-id
        data_id = article.get('data-id')

        # Витягнемо дату з <datetime>
        date_tag = article.find('datetime')
        date = date_tag.get_text(strip=True) if date_tag else datetime.now().strftime('%Y-%m-%d')

        # Витягнемо заголовок з <h2> та посилання з <a>
        h2_tag = article.find('h2')
        if h2_tag:
            link_tag = h2_tag.find('a')
            title = link_tag.get_text(strip=True) if link_tag else "No title"
            link = link_tag['href'] if link_tag else "No link"
        else:
            title, link = "No title", "No link"

        # Витягнемо короткий опис з <p>
        p_tag = article.find('p')
        summary = p_tag.get_text(strip=True) if p_tag else "No summary"

        # Додаємо знайдені дані в список новин
        news_list.append({
            'title': title,
            'link': link,
            'date': date,
            'summary': summary,
            'data_id': data_id  # додаємо data-id
        })

    return news_list


def save_to_csv(data: List[Dict[str, str]], filename: str = 'news.csv') -> None:
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
            writer = csv.DictWriter(file, fieldnames=['data_id', 'title', 'link', 'date', 'summary'])
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"News saved to {filename}")
    except Exception as e:
        error_message = handle_file_error('write', filename, e)
        logger.error(error_message)


if __name__ == '__main__':
    URL = "https://www.ukrinform.ua/block-lastnews?page=60"  # Введіть URL сторінки, з якої хочете отримати новини
    soup = get_page(URL)
    if soup:
        news_data = parse_news(soup)
        save_to_csv(news_data)
