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
                              error: Exception = None, status_code: int = None) -> str:
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
    if error:
        if isinstance(error, aiohttp.ClientConnectionError):
            error_message = f"Connection error while {action} {url}"
            logger.error(error_message)
            return error_message
        elif isinstance(error, aiohttp.ClientTimeout):
            error_message = f"Timeout error while {action} {url}"
            logger.error(error_message)
            return error_message
        elif isinstance(error, aiohttp.ClientResponseError):
            error_message = f"Response error while {action} {url}, Status: {error.status}"
            logger.error(error_message)
            return error_message
        if isinstance(error, aiohttp.ClientPayloadError):
            error_message = f"Payload error while {action} {url}"
            logger.error(error_message)
            return error_message
        else:
            error_message = f"Unexpected error while {action} {url}: {error}"
            logger.error(error_message)
            return error_message
    elif status_code:
        error_message = status_messages.get(status_code, f"Failed with status "
                                                         f"{status_code} during {action}")
        logger.warning(f"{url} - {error_message}")
        return error_message
    return f"Unknown error occurred during {action} {url}"
