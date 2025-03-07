"""
This module tests sending requests to a server using different modes:
    - Synchronous
    - Multi-threaded
    - Multi-processing
    - Asynchronous

The results of each test are logged into 'multi_test_results.log'.

Functions:
    send_request_sync(url: str) -> None:
        Sends a synchronous HTTP request to the provided URL and logs the response status.

    send_request_async(url: str) -> None:
        Sends an asynchronous HTTP request to the provided URL and logs the response status.

    test_sync(url: str, count: int) -> None:
        Runs a test of synchronous requests, sending 'count' requests to the provided URL.

    test_multithreaded(url: str, count: int) -> None:
        Runs a test of multithreaded requests, sending 'count'
        requests concurrently to the provided URL.

    test_multiprocess(url: str, count: int) -> None:
        Runs a test of multiprocessing requests, sending 'count'
        requests concurrently to the provided URL.

    test_async(url: str, count: int) -> None:
        Runs a test of asynchronous requests, sending 'count'
        requests concurrently to the provided URL.

Usage:
    This script cannot be executed directly.
    It is designed to be run through the 'async_web_server.py' script.
    The 'async_web_server.py' script will prompt you to select the test mode.
    Based on the selected mode, the server will initiate the corresponding test,
    and you can observe the results of the requests.
    The URL to test can be modified in the 'async_web_server.py' script.
"""
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio
import requests
import aiohttp
from logger_config import get_logger

logger = get_logger(__name__, "multi_test_results.log")


def send_request_sync(url: str) -> None:
    """
    Sends a synchronous HTTP request to the provided URL and logs the response status.

    Args:
        url (str): The URL to send the request to.

    Returns:
        None
    """
    try:
        response = requests.get(url, timeout=5)
        logger.info("Synchronous: %s %s", response.status_code, response.text)
    except requests.Timeout:
        logger.error("Request timed out for URL: %s", url)
    except requests.RequestException as e:
        logger.error("Error: %s", e)


async def send_request_async(url: str) -> None:
    """
    Sends an asynchronous HTTP request to the provided URL and logs the response status.

    Args:
        url (str): The URL to send the request to.

    Returns:
        None
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            logger.info("Async: %s %s", response.status, text)


def test_sync(url: str, count: int) -> None:
    """
    Runs a test of synchronous requests, sending 'count' requests to the provided URL.

    Args:
        url (str): The URL to send the requests to.
        count (int): The number of requests to send.

    Returns:
        None
    """
    start = time.time()
    for _ in range(count):
        send_request_sync(url)
    total_time = time.time() - start
    logger.info("Synchronous mode took %.2f sec", total_time)


def test_multithreaded(url: str, count: int) -> None:
    """
    Runs a test of multithreaded requests, sending 'count'
    requests concurrently to the provided URL.

    Args:
        url (str): The URL to send the requests to.
        count (int): The number of requests to send.

    Returns:
        None
    """
    start = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(send_request_sync, [url] * count)
    total_time = time.time() - start
    logger.info("Multi-threaded mode took %.2f sec", total_time)


def test_multiprocess(url: str, count: int) -> None:
    """
    Runs a test of multiprocessing requests, sending 'count'
    requests concurrently to the provided URL.

    Args:
        url (str): The URL to send the requests to.
        count (int): The number of requests to send.

    Returns:
        None
    """
    start = time.time()
    with ProcessPoolExecutor() as executor:
        executor.map(send_request_sync, [url] * count)
    total_time = time.time() - start
    logger.info("Multi-process mode took %.2f sec", total_time)


async def test_async(url: str, count: int) -> None:
    """
    Runs a test of asynchronous requests, sending 'count'
    requests concurrently to the provided URL.

    Args:
        url (str): The URL to send the requests to.
        count (int): The number of requests to send.

    Returns:
        None
    """
    start = time.time()
    tasks = [send_request_async(url) for _ in range(count)]
    await asyncio.gather(*tasks)
    total_time = time.time() - start
    logger.info("Asynchronous mode took %.2f sec", total_time)


if __name__ == "__main__":
    URL = "http://127.0.0.1:7777/slow"
    COUNT = 500
    test_sync(URL, COUNT)
    test_multithreaded(URL, COUNT)
    test_multiprocess(URL, COUNT)
    asyncio.run(test_async(URL, COUNT))
