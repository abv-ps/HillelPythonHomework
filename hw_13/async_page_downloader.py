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

UrlList = list[str]


async def download_page(url: str) -> None:
    """
    Simulates downloading a page by waiting for a random time between 1 and 5 seconds
    and then checks the status of the HTTP response.

    Args:
        url (str): The URL of the page to download.
    """
    # Random delay between 1 and 5 seconds to simulate downloading
    delay = random.randint(1, 5)
    await asyncio.sleep(delay)  # Wait for the random delay

    # Now simulate the page download using aiohttp
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    print(f"Successfully downloaded {url} in {delay} seconds "
                          f"with status code {response.status}")
                elif response.status == 403:
                    print(f"Error 403: Forbidden while downloading {url}")
                elif response.status == 404:
                    print(f"Error 404: Not Found while downloading {url}")
                elif response.status == 504:
                    print(f"Error 504: Gateway Timeout while downloading {url}")
                else:
                    print(f"Failed to download {url} in {delay} seconds "
                          f"with status code {response.status}")
        except aiohttp.ClientConnectionError:
            print(f"Connection error while downloading {url}")
        except aiohttp.ClientTimeout:
            print(f"Timeout error while downloading {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")


async def main(urls: UrlList) -> None:
    """
    Downloads multiple pages concurrently.

    Args:
        urls (list[str]): A list of URLs to download.
    """
    await asyncio.gather(*(download_page(url) for url in urls))

if __name__ == "__main__":
    urls_to_download = [
        "https://www.example.com",
        "https://www.python.org",
        "https://www.github.com"
    ]
    asyncio.run(main(urls_to_download))
