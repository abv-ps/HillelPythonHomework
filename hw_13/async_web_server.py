"""
Asynchronous Web Server with User File Selection and Auto-Shutdown

This module implements an asynchronous web server using aiohttp.
It allows the user to select a test script before starting.
After processing test requests, the server shuts down automatically.

Routes:
    - "/"        -> Returns "Hello, World!" instantly.
    - "/slow"    -> Simulates a slow operation (5 seconds delay).

Features:
    - Asynchronous request handling.
    - Logging of incoming requests and responses.
    - Auto-shutdown after processing test requests.
    - User selects a test file before server start.
"""

import asyncio
import os
import subprocess
import sys
from aiohttp import web
from logger_config import get_logger

logger = get_logger(__name__, "server_requests.log")


async def handle_root(request: web.Request) -> web.Response:
    """
    Handles requests to the root ("/") route.

    Args:
        request (web.Request): The incoming request.

    Returns:
        web.Response: A response with the text "Hello, World!".
    """
    logger.info("Received request at '/'")
    return web.Response(text="Hello, World!")


async def handle_slow(request: web.Request) -> web.Response:
    """
    Handles requests to the "/slow" route with a simulated delay.

    Simulates a slow operation with a 5-second delay.

    Args:
        request (web.Request): The incoming request.

    Returns:
        web.Response: A response with the text "Operation completed".
    """
    logger.info("Received request at '/slow', simulating delay...")
    await asyncio.sleep(5)
    logger.info("Completed slow task.")
    return web.Response(text="Operation completed")


async def create_app() -> web.Application:
    """
    Creates and returns an aiohttp application with routes configured.

    Returns:
        web.Application: The aiohttp application.
    """
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/slow", handle_slow)
    return app


async def run_test_script(test_file: str) -> None:
    """
    Runs a test script asynchronously.

    Args:
        test_file (str): The path to the test script.
    """
    logger.info(f"Running test script: {test_file}")

    process = await asyncio.create_subprocess_exec(
        sys.executable, test_file,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        logger.info(f"Test script {test_file} completed successfully.")
    else:
        logger.error(f"Test script {test_file} failed with error: {stderr.decode()}")


async def run_server() -> None:
    """
    Runs the web server and shuts it down after executing the test script.

    The server starts at http://127.0.0.1:7777 and waits for incoming requests.
    After processing the test script, the server shuts down automatically.
    """
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="127.0.0.1", port=7777)
    await site.start()

    logger.info("Server started on http://127.0.0.1:7777")
    await asyncio.sleep(0.5)
    test_file = select_test_file()
    if test_file:
        await run_test_script(test_file)

    await asyncio.sleep(3)

    logger.info("Shutting down server...")
    await runner.cleanup()


def select_test_file() -> str | None:
    """
    Allows the user to select a test script before starting the server.

    This function lists available Python files in the current directory
    and prompts the user to select one.

    Returns:
        str | None: The path to the selected test file, or None if no valid file is selected.
    """
    test_folder = os.getcwd()
    print(f"Select a test script from {test_folder}:")

    test_files = [f for f in os.listdir(test_folder)
                  if f.endswith(".py") and f != "async_web_server.py"]

    if not test_files:
        logger.info("No test scripts found in the directory.")
        return None

    for i, file in enumerate(test_files, start=1):
        print(f"{i}: {file}")

    try:
        choice = int(input("Enter the number of the test script: ")) - 1
        if choice < 0 or choice >= len(test_files):
            raise ValueError
    except ValueError:
        logger.info("Invalid selection.")
        return None

    return os.path.join(test_folder, test_files[choice])


if __name__ == "__main__":
    asyncio.run(run_server())
