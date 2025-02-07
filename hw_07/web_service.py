"""Module for fetching data from a web service with error handling."""

import logging
import requests
import unittest
from unittest.mock import patch

# Налаштування логування
logging.basicConfig(level=logging.ERROR)


class WebService:
    """Class for fetching data from a web service."""

    def get_data(self, url: str) -> dict:
        """
        Fetch data from the given URL.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            dict: The JSON response or an error message.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return {"error": str(http_err)}
        except requests.exceptions.RequestException as err:
            logging.error(f"Network error occurred: {err}")
            return {"error": str(err)}


class TestWebService(unittest.TestCase):
    """Unit tests for WebService class."""

    @patch('requests.get')
    def test_get_data_success(self, mock_get):
        """Test a successful API response."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}

        service = WebService()
        result = service.get_data('https://some.com')

        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once_with('https://some.com')

    @patch('requests.get')
    def test_get_data_404_error(self, mock_get):
        """Test API response with a 404 error."""
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")

        service = WebService()
        result = service.get_data('https://some.com')

        self.assertEqual(result, {"error": "404 Client Error: Not Found"})
        mock_get.assert_called_once_with('https://some.com')

    @patch('requests.get')
    def test_get_data_500_error(self, mock_get):
        """Test API response with a 500 error."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error: Internal Server Error")

        service = WebService()
        result = service.get_data('https://some.com')

        self.assertEqual(result, {"error": "500 Server Error: Internal Server Error"})
        mock_get.assert_called_once_with('https://some.com')

    @patch('requests.get')
    def test_get_data_other_error(self, mock_get):
        """Test API response when a network error occurs."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        service = WebService()
        result = service.get_data('https://some.com')

        self.assertEqual(result, {"error": "Network error"})
        mock_get.assert_called_once_with('https://some.com')


if __name__ == '__main__':
    unittest.main()
