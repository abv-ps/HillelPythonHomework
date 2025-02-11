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

import requests
import asyncio
import logging
import unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.ERROR)


class WebService:
    """
    Class for fetching data from a web service.

    This class provides methods for synchronous and asynchronous HTTP requests.
    """

    def __init__(self) -> None:
        """
        Initialize WebService with a thread pool executor.
        """
        self.executor = ThreadPoolExecutor()

    def fetch_data_sync(self, url: str) -> Dict[str, Any]:
        """
        Fetch data synchronously using the requests library.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            Dict[str, Any]: The JSON response or an error message.

        Example:
            >>> service = WebService()
            >>> isinstance(service.fetch_data_sync("https://jsonplaceholder.typicode.com/todos/1"), dict)
            True
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return {"error": str(http_err)}
        except requests.exceptions.RequestException as err:
            logging.error(f"Network error occurred: {err}")
            return {"error": str(err)}

    async def fetch_data(self, url: str) -> Dict[str, Any]:
        """
        Fetch data asynchronously using a thread pool executor.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            Dict[str, Any]: The JSON response or an error message.

        Example:
            >>> service = WebService()
            >>> asyncio.run(service.fetch_data("https://jsonplaceholder.typicode.com/todos/1"))  # doctest: +ELLIPSIS
            {'userId': ..., 'id': ..., 'title': ..., 'completed': ...}
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.fetch_data_sync, url)


class TestWebService(unittest.TestCase):
    """Unit tests for WebService class."""

    @patch("requests.get")
    def test_fetch_data_success(self, mock_get):
        """Test a successful API response."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}

        service = WebService()
        result = asyncio.run(service.fetch_data("https://some.com"))

        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with("https://some.com")

    @patch("requests.get")
    def test_fetch_data_404_error(self, mock_get):
        """Test API response with a 404 error."""
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: Not Found")

        service = WebService()
        result = asyncio.run(service.fetch_data("https://some.com"))

        self.assertEqual(result, {"error": "404 Client Error: Not Found"})
        mock_get.assert_called_once_with("https://some.com")

    @patch("requests.get")
    def test_fetch_data_500_error(self, mock_get):
        """Test API response with a 500 error."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "500 Server Error: Internal Server Error")

        service = WebService()
        result = asyncio.run(service.fetch_data("https://some.com"))

        self.assertEqual(result, {"error": "500 Server Error: Internal Server Error"})
        mock_get.assert_called_once_with("https://some.com")

    @patch("requests.get")
    def test_fetch_data_other_error(self, mock_get):
        """Test API response when a network error occurs."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        service = WebService()
        result = asyncio.run(service.fetch_data("https://some.com"))

        self.assertEqual(result, {"error": "Network error"})
        mock_get.assert_called_once_with("https://some.com")


if __name__ == "__main__":
    unittest.main()
