"""
This module provides functionality for simulating the concurrent downloading of pages.

It contains an asynchronous function to simulate downloading a single page
and another asynchronous function to download multiple pages concurrently.

Functions:
    download_page(url: str) -> None:
        Simulates downloading a single page by waiting for a random time between 1 and 5 seconds
        and then checks the status of the HTTP response.

    main(urls: list[str]) -> None:
        Downloads multiple pages concurrently by calling `download_page` for each URL in the list.

Usage:
    This module can be used to simulate the concurrent downloading of pages in an asynchronous manner.
    You can provide a list of URLs to the `main` function, and it will download the pages concurrently,
    simulating realistic delays for each page.
"""

import asyncio
import random
import aiohttp
from logger_config import get_logger
from error_handler import handle_action_error

logger = get_logger(__name__, "downloaded_pages.log")

UrlList = list[str]


async def download_page(url: str) -> None:
    """
    Simulates downloading a page by waiting for a random time between 1 and 5 seconds
    and then checks the status of the HTTP response.

    Args:
        url (str): The URL of the page to download.
    """
    delay = random.randint(1, 5)
    await asyncio.sleep(delay)  # Wait for the random delay


    try:
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        logger.info(f"Successfully downloaded {url} in "
                                    f"{delay} seconds with status code {response.status}")
                    else:
                        await handle_action_error(url, "page_downloading",
                                                  status_code=response.status)
    except Exception as e:
        await handle_action_error(url, "page_downloading", error=e)


async def main(urls: UrlList) -> None:
    """
    Downloads multiple pages concurrently.

    Args:
        urls (list[str]): A list of URLs to download.
    """
    await asyncio.gather(*(download_page(url) for url in urls))


if __name__ == "__main__":
    urls_to_download = [
        "https://www.google.com",
        "https://www.ithillel.ua",
        "https://www.habr.com"
    ]
    asyncio.run(main(urls_to_download))
