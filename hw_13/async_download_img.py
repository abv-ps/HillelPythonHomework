"""
This module provides functionality for downloading images from specified URLs
and saving them to a designated folder. It utilizes asynchronous functions
to download multiple images concurrently, improving efficiency and resource usage.

Functions:
    download_image(url: str, folder: str) -> None:
        Downloads a single image from the provided URL and saves it to the specified folder.
        t handles errors that may occur during the image downloading process.

    download_images(urls: list[str], folder: str) -> None:
        Downloads multiple images concurrently by calling `download_image` for each URL in the list.

    main() -> None:
        Downloads a predefined list of images concurrently by calling `download_images`.

Usage:
    This module can be used to download images from given URLs
    and save them to a specified folder.
    It supports concurrent downloads, allowing efficient downloading
    of multiple images at the same time.
    You can provide a list of URLs to the `main` function or call `download_images`
    with a custom list of URLs.
"""
import os
import asyncio
import aiohttp
from logger_config import get_logger
from error_handler import handle_action_error

logger = get_logger(__name__, "img_download.log")


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
            async with session.get(url) as response:
                if response.status != 200:
                    await handle_action_error(url, "img_downloading", status_code=response.status)
                    return

                filename = os.path.join(folder, url.split('/')[-1])
                os.makedirs(folder, exist_ok=True)

                with open(filename, 'wb') as file:
                    while chunk := await response.content.read(1024):
                        file.write(chunk)

                logger.info("Downloaded: %s", filename)
    except Exception as e:
        await handle_action_error(url, "downloading", error=e)


async def download_images(urls: list[str], folder: str) -> None:
    """
    Downloads multiple images concurrently using asyncio.

    Args:
        urls (list[str]): List of image URLs to download.
        folder (str): The folder where the downloaded images will be saved.
    """
    tasks = [download_image(url, folder) for url in urls]
    await asyncio.gather(*tasks)


async def main() -> None:
    """
    Main function that downloads images from given URLs.
    """
    urls_to_download = [
        "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
        "https://assets.ithillel.ua/images/og/_transform_ogImage/homepage-uk.jpg",
        "https://habrastorage.org/webt/ql/qd/oq/qlqdoql0nbdlwyvqhzcfo0lgfmm.jpeg"
    ]
    download_folder = "downloads"
    await download_images(urls_to_download, download_folder)


if __name__ == "__main__":
    asyncio.run(main())
