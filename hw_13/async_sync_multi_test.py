"""
Test script to send 500 requests using different modes:
    - Synchronous
    - Multi-threaded
    - Multi-processing
    - Asynchronous

Results are logged into test_results.log.
"""

import time
import logging
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Configure logging
logging.basicConfig(filename="test_results.log", level=logging.INFO, format="%(asctime)s - %(message)s")


def send_request_sync(url: str) -> None:
    """Sends a synchronous request."""
    try:
        response = requests.get(url)
        logging.info(f"Synchronous: {response.status_code} {response.text[:30]}")
    except requests.RequestException as e:
        logging.error(f"Error: {e}")


async def send_request_async(url: str) -> None:
    """Sends an asynchronous request."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            logging.info(f"Async: {response.status} {text[:30]}")


def test_sync(url: str, count: int) -> None:
    """Tests synchronous requests."""
    start = time.time()
    for _ in range(count):
        send_request_sync(url)
    logging.info(f"Synchronous mode took {time.time() - start:.2f} sec")


def test_multithreaded(url: str, count: int) -> None:
    """Tests multi-threaded requests."""
    start = time.time()
    with ThreadPoolExecutor() as executor:
        executor.map(send_request_sync, [url] * count)
    logging.info(f"Multi-threaded mode took {time.time() - start:.2f} sec")


def test_multiprocess(url: str, count: int) -> None:
    """Tests multi-processing requests."""
    start = time.time()
    with ProcessPoolExecutor() as executor:
        executor.map(send_request_sync, [url] * count)
    logging.info(f"Multi-process mode took {time.time() - start:.2f} sec")


async def test_async(url: str, count: int) -> None:
    """Tests asynchronous requests."""
    start = time.time()
    tasks = [send_request_async(url) for _ in range(count)]
    await asyncio.gather(*tasks)
    logging.info(f"Asynchronous mode took {time.time() - start:.2f} sec")


if __name__ == "__main__":
    URL = "http://127.0.0.1:7777/slow"

    test_sync(URL, 10)
    test_multithreaded(URL, 10)
    test_multiprocess(URL, 10)
    asyncio.run(test_async(URL, 10))
