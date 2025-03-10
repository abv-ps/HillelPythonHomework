"""
This module is designed to handle various types of errors that can occur
during HTTP operations such as fetching, downloading, and parsing resources.
It provides a function `handle_action_error` to process and log errors related
to network issues, timeouts, response errors, and payload issues. It also
returns detailed error messages based on the specific error type or HTTP
status code encountered.

Dependencies:
    - aiohttp: A Python library used for asynchronous HTTP requests.
    - logger_config: A custom logging module to configure and generate logs for errors.

Key Components:
    1. status_messages Dictionary: A predefined set of status codes and their corresponding
       messages to describe the nature of the HTTP error encountered (e.g., 404 - "Not Found",
       503 - "Service Unavailable").

    2. handle_action_error Function:
        Args:
            url (str): The URL or resource being processed.
            action (str): The action being performed (fetching, downloading, etc.).
            error (Optional[Exception]): The exception object if an error occurs.
            status_code (Optional[int]): The HTTP status code returned, if applicable.

        Returns:
            str: A string containing an error message that describes the error or status.

        Error Handling:
            The function handles specific exceptions raised by the `aiohttp` library, such as
            connection errors, timeouts, response errors, and payload errors.
            If a status code is provided, the function will return an appropriate message
            from the `status_messages` dictionary or a generic error message.

    3. Logging:
        Errors are logged to a file (`action_error.log`) using the `get_logger` utility function.
        The log captures the details of the action, URL, error type, and status code.
"""
from typing import Optional

import aiohttp
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


async def handle_action_error(url: str, action: str,
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

    if error:
        if isinstance(error, aiohttp.ClientConnectionError):
            error_message = f"Connection error while {action} {url}, Status: {error}"
            logger.error(error_message)
        if isinstance(error, aiohttp.ClientTimeout):
            error_message = f"Timeout error while {action} {url}, Status: {error}"
            logger.error(error_message)
        if isinstance(error, aiohttp.ClientResponseError):
            error_message = f"Response error while {action} {url}, Status: {error}"
            logger.error(error_message)
        if isinstance(error, aiohttp.ClientPayloadError):
            error_message = f"Payload error while {action} {url}, Status: {error}"
            logger.error(error_message)
        error_message = f"Unexpected error while {action} {url}, Status: {error}"
        logger.error(error_message)

    if status_code and not error_message:
        error_message = status_messages.get(status_code,
                                            f"Failed with status {status_code} "
                                            f"during {action} - {url}")
        logger.warning("%s - Status Code: %s - %s", url, status_code, error_message)

    if not error_message:
        error_message = f"Unknown error occurred during {action} - {url}"

    return error_message
