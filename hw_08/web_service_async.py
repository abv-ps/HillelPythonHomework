"""
WebService module for fetching data from a web service.

This module provides both synchronous and asynchronous methods
to fetch JSON data from a given URL. The asynchronous method uses
a thread pool executor to handle network requests without blocking
the event loop.

Example usage:
    >>> service = WebService()
    >>> import asyncio
    >>> asyncio.run(service.fetch_data("https://example.com"))
"""

import asyncio
import logging
import unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Union
import requests

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s '
                                                '- %(levelname)s - %(message)s')


class WebService:
    """
    Class for fetching data from a web service.

    This class provides methods for synchronous and asynchronous HTTP requests.
    """

    def __init__(self, max_workers: int = 7) -> None:
        """
        Initialize WebService with a thread pool executor.

        Args:
            max_workers (int): The maximum number of worker threads.
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def fetch_data_sync(self, url: str) -> Union[Dict[str, Any], Dict[str, str]]:
        """
        Fetch data synchronously using the requests library.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            Union[Dict[str, Any], Dict[str, str]]: The JSON response or an error message.

        Example:
            >>> service = WebService()
            >>> isinstance(service.fetch_data_sync("https://jsonplaceholder.typicode.com/todos/1"), dict)
            True
        """
        try:
            logging.info("Fetching data from %s", url)
            response = requests.get(url, timeout=(5, 10))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error("HTTP error occurred while fetching %s: %s", url, http_err)
            return {"error": str(http_err)}
        except requests.exceptions.RequestException as err:
            logging.error("Network error occurred while fetching %s: %s", url, err)
            return {"error": str(err)}
        except Exception as ex:
            logging.error("Unexpected error while fetching %s: %s", url, ex)
            return {"error": "Unexpected error occurred"}

    async def fetch_data(self, url: str) -> Union[Dict[str, Any], Dict[str, str]]:
        """
        Fetch data asynchronously using a thread pool executor.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            Union[Dict[str, Any], Dict[str, str]]: The JSON response or an error message.

        Example:
            >>> service = WebService()
            >>> asyncio.run(service.fetch_data("https://jsonplaceholder.typicode.com/todos/1"))  # doctest: +ELLIPSIS
            {'userId': ..., 'id': ..., 'title': ..., 'completed': ...}
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.fetch_data_sync, url)


class TestWebService(unittest.IsolatedAsyncioTestCase):
    """Unit tests for WebService class."""

    async def asyncSetUp(self) -> None:
        """Set up the WebService instance before each test."""
        self.service = WebService()

    @patch("requests.get")
    async def test_fetch_data_success(self, mock_get):
        """Test a successful API response."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}

        result = await self.service.fetch_data("https://some.com")

        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with("https://some.com", timeout=(5, 10))

    @patch("requests.get")
    async def test_fetch_data_404_error(self, mock_get):
        """Test API response with a 404 error."""
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: Not Found"
        )

        result = await self.service.fetch_data("https://some.com")

        self.assertEqual(result, {"error": "404 Client Error: Not Found"})
        mock_get.assert_called_once_with("https://some.com", timeout=(5, 10))

    @patch("requests.get")
    async def test_fetch_data_500_error(self, mock_get):
        """Test API response with a 500 error."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "500 Server Error: Internal Server Error"
        )

        result = await self.service.fetch_data("https://some.com")

        self.assertEqual(result, {"error": "500 Server Error: Internal Server Error"})
        mock_get.assert_called_once_with("https://some.com", timeout=(5, 10))

    @patch("requests.get")
    async def test_fetch_data_other_error(self, mock_get):
        """Test API response when a network error occurs."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = await self.service.fetch_data("https://some.com")

        self.assertEqual(result, {"error": "Network error"})
        mock_get.assert_called_once_with("https://some.com", timeout=(5, 10))


if __name__ == "__main__":
    unittest.main()