"""
This module demonstrates how to simulate multiple client requests
with both fast and slow responses using asyncio and aiohttp.

The `simulate_requests` function simulates several HTTP requests to a server,
both to fast and slow endpoints.
It logs the responses to the server in both the terminal and a log file.
Each request is initiated concurrently, and
the responses are processed asynchronously.

Functions:
    - simulate_requests() -> None:
        Simulates multiple asynchronous HTTP requests and logs the responses.

Usage:
    This script cannot be executed directly.
    It is designed to be run through the 'async_web_server.py' script.
    The 'async_web_server.py' script will prompt you to select the test mode.
    Based on the selected mode, the server will initiate the corresponding test,
    and you can observe the results of the requests.
    The URL to test can be modified in the 'async_web_server.py' script.
"""

import asyncio
import aiohttp
from logger_config import get_logger

logger = get_logger(__name__, "simulate_requests.log")

async def simulate_requests() -> None:
    """
    Simulates multiple HTTP requests with both fast and slow responses.

    This function creates asynchronous HTTP GET requests to multiple URLs (both fast and slow).
    It uses asyncio to execute the requests concurrently.
    Responses are logged to a file and the terminal.
    """
    logger.info("Starting to simulate multiple client requests.")

    timeout = aiohttp.ClientTimeout(total=5)  # Set timeout for each request
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            session.get('http://127.0.0.1:7777/'),
            session.get('http://127.0.0.1:7777/slow'),
            session.get('http://127.0.0.1:7777/'),
            session.get('http://127.0.0.1:7777/slow'),
            session.get('http://127.0.0.1:7777/'),
            session.get('http://127.0.0.1:7777/slow'),
            session.get('http://127.0.0.1:7777/')
        ]

        # Gather and execute all requests concurrently
        responses = await asyncio.gather(*tasks)

        # Process the responses and log them
        for response in responses:
            content = await response.text()
            # Log the first 30 characters of the response
            logger.info("Received response: %s...", content[:30])

    logger.info("Finished all simulated requests.")

if __name__ == "__main__":
    asyncio.run(simulate_requests())
