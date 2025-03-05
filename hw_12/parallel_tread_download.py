"""
Module for downloading files from given URLs and saving them to a specified folder.

This module provides functions for downloading one or multiple files concurrently using threads.
It also includes a mock version of the `requests.get` function for simulating downloads during testing.

Functions:
    download_file(url: str, folder: str) -> None:
        Downloads a single file from a given URL and saves it to the specified folder.

    download_files(urls: list[str], folder: str) -> None:
        Downloads multiple files concurrently using threads and saves them to the specified folder.

    mock_requests_get(url: str, stream: bool = False) -> Any:
        Mocks the `requests.get` call to simulate downloading files for testing purposes.

    main() -> None:
        Simulates downloading files from predefined URLs using a mock for `requests.get`.
"""


import os
import threading
import requests
from unittest.mock import patch, Mock


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


def mock_requests_get(url, stream=False):
    """
    Mocks the requests.get call to simulate downloading files.

    This function returns a mock response object that simulates a real
    HTTP request. The mock object has methods like `raise_for_status` and
    `iter_content` for testing without actually downloading files.

    Args:
        url (str): The URL for which the request is being mocked.
        stream (bool): If True, the request is mocked with the stream parameter.

    Returns:
        Any: The mocked response object with mocked methods.
    """
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.iter_content.return_value = [b"Fake content for testing"]
    return mock_response


def main():
    """
    Main function that simulates downloading files from given URLs.

    This function defines a list of URLs to download, and then it uses
    the `patch` method to replace the original `requests.get` with a mocked version.
    The files are "downloaded" to a specified folder using the `download_files` function.

    No actual files are downloaded, as the requests are mocked for testing purposes.
    """
    urls_to_download = [
        "https://example.com/file1.txt",
        "https://example.com/file2.jpg",
        "https://example.com/file3.zip"
    ]
    download_folder = "downloads"

    # Using patch to replace the original requests.get with our mock
    with patch('requests.get', side_effect=mock_requests_get):
        download_files(urls_to_download, download_folder)


if __name__ == "__main__":
    main()
