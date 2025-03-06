"""
This module provides functions for downloading images from given URLs.

It includes functionalities to:
- Download a single image from a specified URL and save it to a local folder.
- Download multiple images concurrently using asyncio.
- Mock HTTP requests for testing purposes.

The module makes use of `aiohttp` for asynchronous HTTP requests, `asyncio` for concurrency,
and includes a custom error handler to manage issues that might arise during the download process.

Functions:
- download_image(url: str, folder: str) -> None: Downloads a single image from a URL
  and saves it to a folder.
- download_images(urls: list[str], folder: str) -> None: Downloads multiple images concurrently
  from a list of URLs.
- mock_requests_get(url, stream=False) -> aiohttp.ClientResponse:
  Mocks the `aiohttp` HTTP GET request for testing purposes.
- main() -> None: Entry point for running the module, simulates downloading images.

Usage:
- To use this module, call the `download_images()` function
  with a list of URLs and a destination folder.
"""
import os
import asyncio
import aiohttp
from unittest.mock import patch, AsyncMock
from logger_config import get_logger
from error_handler import handle_action_error

logger = get_logger(__name__, "download.log")


async def download_image(url: str, folder: str) -> None:
    """
    Downloads an image from a given URL and saves it to the specified folder.

    Args:
        url (str): The URL of the image to download.
        folder (str): The folder where the downloaded image will be saved.

    Raises:
        Exception: If there is an error during the image downloading process.
    """
    try:
        async with aiohttp.ClientSession() as session:
            response = await mock_requests_get(url)
            async with response:
                if response.status != 200:
                    await handle_action_error(url, "img_downloading", status_code=response.status)
                    return

                filename = os.path.join(folder, url.split('/')[-1])
                with open(filename, 'wb') as file:
                    while chunk := await response.content.read(1024):
                        file.write(chunk)

                logger.info(f"Downloaded: {filename}")
    except Exception as e:
        await handle_action_error(url, "downloading", error=e)


async def download_images(urls: list[str], folder: str) -> None:
    """
    Downloads multiple images concurrently using asyncio.

    Args:
        urls (list[str]): List of image URLs to download.
        folder (str): The folder where the downloaded images will be saved.

    Raises:
        Exception: If there is an error while downloading one or more images.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    tasks = [download_image(url, folder) for url in urls]
    await asyncio.gather(*tasks)


async def mock_requests_get(url: str, stream: bool = False) -> aiohttp.ClientResponse:
    """
    An asynchronous mock for `aiohttp.ClientSession.get` to simulate an HTTP request.

    Args:
        url (str): The URL to mock the request for.
        stream (bool): Whether the request should be treated as a streaming request (default is False).

    Returns:
        aiohttp.ClientResponse: A mocked response simulating a successful HTTP request.
    """
    await asyncio.sleep(0.1)  # Simulate network delay

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.raise_for_status = AsyncMock()
    mock_response.__aenter__.return_value = mock_response
    mock_response.__aexit__.return_value = AsyncMock()

    mock_response.content = AsyncMock()
    mock_response.content.read = AsyncMock(side_effect=[b"Fake image content", b""])

    return mock_response


async def main() -> None:
    """
    Main function that simulates downloading images from given URLs.

    This function defines a list of URLs to download, and then it uses
    the `patch` method to replace the original `aiohttp.ClientSession().get`
    with a mocked version.

    Raises:
        Exception: If an error occurs while downloading images.
    """
    urls_to_download = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg"
    ]
    download_folder = "downloads"

    with patch('aiohttp.ClientSession.get', new=AsyncMock(side_effect=mock_requests_get)):
        await download_images(urls_to_download, download_folder)


if __name__ == "__main__":
    asyncio.run(main())
