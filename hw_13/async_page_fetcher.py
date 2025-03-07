"""
This module provides functionality to perform asynchronous HTTP requests
to fetch page content from a list of URLs. It handles various HTTP status codes
and logs the results to both a log file and the console.

It contains the following functions:

    fetch_content(url: str) -> str:
        Performs an HTTP request to the given URL and returns the page content
        or an error message based on the response status. The function handles
        various HTTP status codes (e.g., 200, 403, 404, 503) and connection errors.

    fetch_all(urls: list[str]) -> list[str]:
        Fetches multiple pages concurrently using `fetch_content` for each URL.

    main(urls: list[str]) -> None:
        Downloads multiple pages concurrently and prints the content or error messages.

Usage:
    This module can be run directly, providing a list of URLs to download and
    fetch their content concurrently. The results are logged to a file and printed to the console.
"""
import asyncio
import aiohttp

from error_handler import handle_action_error
from logger_config import get_logger

logger = get_logger(__name__, "fetched_pages.log")

UrlList = list[str]


async def fetch_content(url: str) -> str:
    """
    Performs an HTTP request to the given URL and returns the page content.
    Handles potential connection errors.

    Args:
        url: The URL of the page to fetch.

    Returns:
        The content of the page or an error message.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    logger.info("Successfully fetched %s (Status 200)", url)
                    return await response.text()

                return await handle_action_error(url, action="fetching",
                                                 status_code=response.status)
    except Exception as e:
        return await handle_action_error(url, action="fetching", error=e)



async def fetch_all(urls: UrlList) -> list[str]:
    """
    Fetches multiple pages concurrently.

    Args:
        urls: A list of URLs to fetch.

    Returns:
        A list of page contents or error messages.
    """
    return await asyncio.gather(*(fetch_content(url) for url in urls))


async def main(urls: UrlList) -> None:
    """
    Downloads multiple pages concurrently and prints the result.

    Args:
        urls: A list of URLs to download.
    """
    contents = await fetch_all(urls)
    for url, content in zip(urls, contents):
        # For better representation, only process the first 1000 characters
        print(f"--- {url} ---\n{content[:1000]}...\n")


if __name__ == "__main__":
    urls_to_download = [
        "https://www.google.com",
        "https://www.ithillel.ua",
        "https://www.habr.com"
    ]
    asyncio.run(main(urls_to_download))
