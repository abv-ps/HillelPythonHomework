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
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("fetched_pages.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

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
    status_messages = {
        204: "No content found (Status 204)",
        206: "Partial content returned (Status 206)",
        301: "Redirected permanently (Status 301)",
        401: "Unauthorized access (Status 401)",
        403: "Forbidden access (Status 403)",
        404: "Not found (Status 404)",
        408: "Request timed out (Status 408)",
        413: "Payload too large (Status 413)",
        503: "Service unavailable (Status 503)",
        505: "HTTP version not supported (Status 505)"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    logger.info(f"Successfully fetched {url} (Status 200)")
                    return await response.text()

                error_message = status_messages.get(response.status, f"Failed with status {response.status}")
                logger.warning(f"{url} - {error_message}")
                return error_message
    except aiohttp.ClientConnectionError as e:
        error_connection = f"Connection error while fetching {url}"
        logger.error(error_connection)
        return error_connection
    except aiohttp.ClientTimeout as e:
        error_timeout = f"Timeout error while fetching {url}"
        logger.error(error_timeout)
        return error_timeout
    except Exception as e:
        error_msg = f"Unexpected error while fetching {url}"
        logger.error(error_msg.format(url=url, error=e))
        return error_msg.format(url=url, error=e)


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
        #For better representation, only process the first 1000 characters
        print(f"--- {url} ---\n{content[:1000]}...\n")


if __name__ == "__main__":
    urls_to_download = [
        "https://www.example.com",
        "https://www.python.org",
        "https://www.github.com"
    ]
    asyncio.run(main(urls_to_download))
