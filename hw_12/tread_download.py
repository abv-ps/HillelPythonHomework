"""
Module for downloading files from given URLs and saving them to a specified folder.

This module provides functions for downloading one or multiple files concurrently using threads.

Functions:
    download_file(url: str, folder: str) -> None:
        Downloads a single file from a given URL and saves it to the specified folder.

    download_files(urls: list[str], folder: str) -> None:
        Downloads multiple files concurrently using threads and saves them to the specified folder.
"""

import os
import threading
import requests


def download_file(url: str, folder: str) -> None:
    """
    Downloads a file from a given URL and saves it to the specified folder.

    Args:
        url (str): The URL of the file to download.
        folder (str): The folder where the downloaded file will be saved.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        filename = os.path.join(folder, url.split('/')[-1])

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        print(f"Downloaded: {filename}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")


def download_files(urls: list[str], folder: str) -> None:
    """
    Downloads multiple files concurrently using threads.

    Args:
        urls (list[str]): List of file URLs to download.
        folder (str): The folder where the downloaded files will be saved.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    threads = []
    for url in urls:
        thread = threading.Thread(target=download_file, args=(url, folder))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All downloads completed.")


if __name__ == "__main__":
    urls_to_download = [
        "https://example.com/file1.jpg",
        "https://example.com/file2.pdf",
        "https://example.com/file3.zip"
    ]
    download_folder = "downloads"

    download_files(urls_to_download, download_folder)
