"""
This module is designed to handle various types of errors that can occur
during both HTTP operations (such as fetching, downloading, and parsing
resources) and file operations (such as opening, reading, or writing files).
It provides the `handle_action_error` function to process and log errors
related to network issues, timeouts, response errors, and payload issues
for HTTP operations. Additionally, it includes the `handle_file_error`
function for handling errors related to file system operations. The module
returns detailed error messages based on the specific error type or HTTP
status code encountered, as well as error information for file handling.

Dependencies:
    - requests: A Python library used for HTTP requests.
    - logger_config: A custom logging module to configure and generate logs
      for errors.

Key Components:
    1. `status_messages` Dictionary: A predefined set of status codes and
       their corresponding messages to describe the nature of the HTTP error
       encountered (e.g., 404 - "Not Found", 503 - "Service Unavailable").

    2. `handle_action_error` Function:
        Args:
            url (str): The URL or resource being processed.
            action (str): The action being performed (fetching, downloading, etc.).
            error (Optional[Exception]): The exception object if an error occurs.
            status_code (Optional[int]): The HTTP status code returned, if applicable.

        Returns:
            str: A string containing an error message that describes the error
                 or status.

        Error Handling:
            The function handles specific exceptions raised by the `requests`
            library, such as connection errors, timeouts, response errors,
            and payload errors. If a status code is provided, the function
            will return an appropriate message from the `status_messages` dictionary
            or a generic error message.

    3. `handle_file_error` Function:
        Args:
            action (str): The operation being performed (e.g., 'open', 'read', 'write').
            file_path (str): The path to the file where the error occurred.
            error (Exception): The exception that was raised during the operation.

        Returns:
            str: The error message that will be logged.

        Error Handling:
            The function handles errors related to file operations, such as
            file not found, permission errors, or incorrect file types. It
            logs the details of the error, including the action, file path,
            and error message.

    4. Logging:
        Errors are logged to a file (`action_error.log`) using the `get_logger`
        utility function. The log captures the details of the action, URL,
        error type, status code, or file-related error details.
"""
import csv
from typing import Optional
import aiohttp
from bs4 import FeatureNotFound
import requests
from logger_config import get_logger

logger = get_logger(__name__, "action_error.log")

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


def handle_action_error(url: str, action: str,
                        error: Optional[Exception] = None,
                        status_code: Optional[int] = None) -> str:
    """
    Handles various types of errors that can occur
    during an HTTP operation (fetch, download, parse).

    Args:
        url: The URL or resource being processed.
        action: The action being performed (fetching, downloading, parsing, etc.).
        error: The exception that was raised (if any).
        status_code: The HTTP status code (if any).

    Returns:
        A string containing the error message.
    """
    error_message = None

    if status_code and not error_message:
        error_message = status_messages.get(status_code,
                                            f"Failed with status {status_code} during {action} - {url}")
        logger.warning("%s - Status Code: %s - %s", url, status_code, error_message)

    if error:
        if isinstance(error, aiohttp.ClientError):
            error_message = f"HTTP client error while {action} {url}, Status: {error}"
            logger.error(error_message)
        elif isinstance(error, requests.ConnectionError):
            error_message = f"Connection error while {action} {url}, Status: {error}"
            logger.error(error_message)
        elif isinstance(error, requests.Timeout):
            error_message = f"Timeout error while {action} {url}, Status: {error}"
            logger.error(error_message)
        elif isinstance(error, requests.HTTPError):
            error_message = f"Response error while {action} {url}, Status: {error}"
            logger.error(error_message)
        elif isinstance(error, requests.RequestException):
            error_message = f"Payload error while {action} {url}, Status: {error}"
            logger.error(error_message)
        elif isinstance(error, FeatureNotFound):
            error_message = f"BeautifulSoup parser error while {action} {url}, Status: {error}"
            logger.error(error_message)
        else:
            error_message = f"Unexpected error while {action} {url}, Status: {error}"
            logger.error(error_message)

    if not error_message:
        error_message = f"Unknown error occurred during {action} - {url}"

    return error_message


def handle_file_error(action: str, file_path: str, error: Exception) -> str:
    """
    Handles errors related to file operations, such as opening, reading,
    or writing files.

    Args:
        action: The operation being performed (e.g., 'open', 'read', 'write').
        file_path: The path to the file where the error occurred.
        error: The exception that was raised during the operation.

    Returns:
        The error message that will be logged.
    """
    if isinstance(error, FileNotFoundError):
        error_message = f"File not found error while {action} {file_path}, Error: {error}"
        logger.error(error_message)
    elif isinstance(error, PermissionError):
        error_message = f"Permission denied while {action} {file_path}, Error: {error}"
        logger.error(error_message)
    elif isinstance(error, IsADirectoryError):
        error_message = (f"Attempted to open a directory as a file while {action} {file_path}, "
                         f"Error: {error}")
        logger.error(error_message)
    elif isinstance(error, OSError):
        error_message = f"Operating system error while {action} {file_path}, Error: {error}"
        logger.error(error_message)
    elif isinstance(error, IOError):
        error_message = f"I/O error while {action} {file_path}, Error: {error}"
        logger.error(error_message)
    elif isinstance(error, ValueError):
        error_message = f"Value error while {action} {file_path}, Error: {error}"
        logger.error(error_message)
    elif isinstance(error, csv.Error):
        error_message = f"CSV error while {action} {file_path}, Error: {error}"
        logger.error(error_message)
    elif isinstance(error, UnicodeDecodeError):
        error_message = f"Unicode decode error while {action} {file_path}, Error: {error}"
        logger.error(error_message)
    else:
        error_message = f"Unexpected file error while {action} {file_path}, Error: {error}"
        logger.error(error_message)

    return error_message
