import os
from typing import Optional

import aiohttp
from logger_config import get_logger

logger = get_logger(__name__, "action_error.log")

def shutdown_logger() -> None:
    """Closes all handlers for the logger to release the file lock."""
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)

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
                              error: Optional[Exception] = None, status_code: Optional[int] = None) -> str:
    """
    Handles various types of errors that can occur during an HTTP operation (fetch, download, parse).

    Args:
        url: The URL or resource being processed.
        action: The action being performed (fetching, downloading, parsing, etc.).
        error: The exception that was raised (if any).
        status_code: The HTTP status code (if any).

    Returns:
        A string containing the error message.
    """
    try:
        if error:
            if isinstance(error, aiohttp.ClientConnectionError):
                error_message = "Connection error while %s %s, Status: %s" % (action, url, error)
                logger.error(error_message)
                return error_message
            elif isinstance(error, aiohttp.ClientTimeout):
                error_message = "Timeout error while %s %s, Status: %s" % (action, url, error)
                logger.error(error_message)
                return error_message
            elif isinstance(error, aiohttp.ClientResponseError):
                error_message = "Response error while %s %s, Status: %s" % (action, url, error.status)
                logger.error(error_message)
                return error_message
            elif isinstance(error, aiohttp.ClientPayloadError):
                error_message = "Payload error while %s %s, Status: %s" % (action, url, error)
                logger.error(error_message)
                return error_message
            else:
                error_message = "Unexpected error while %s %s: %s" % (action, url, error)
                logger.error(error_message)
                await cleanup_log_file("action_error.log")
                return error_message
        elif status_code:
            error_message = status_messages.get(status_code, "Failed with status %s during %s" % (status_code, action))
            logger.warning("%s - Status Code: %s - %s" % (url, status_code, error_message))
            return error_message

        return "Unknown error occurred during %s %s" % (action, url)
    finally:
        # Clean up the log file after all processing is done
        logger.info("Performing log file cleanup...")
        await cleanup_log_file("action_error.log")


async def cleanup_log_file(log_file: str) -> None:
    """
    Cleans up the log file by checking its size and removing it if it is empty.

    Args:
        log_file: The path to the log file to be checked and possibly deleted.

    Returns:
        None
    """
    logger.info("Checking if the log file '%s' exists.", log_file)

    if os.path.exists(log_file):
        logger.info("File '%s' exists.", log_file)

        file_size = os.path.getsize(log_file)
        logger.info("File size of '%s': %d bytes.", log_file, file_size)

        if file_size == 0:
            try:
                shutdown_logger()
                open(log_file, 'w').close()
                logger.info("Log file '%s' was empty and has been cleared.", log_file)
            except Exception as e:
                logger.error("Failed to delete the file '%s': %s", log_file, e)
        else:
            logger.info("Log file '%s' is not empty, size: %d bytes.", log_file, file_size)
    else:
        logger.warning("Log file '%s' does not exist.", log_file)

