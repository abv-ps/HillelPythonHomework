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
import logging
import os
import subprocess
import sys
from aiohttp import web

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("server_requests.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


async def handle_root(request: web.Request) -> web.Response:
    """Handles requests to the root ("/") route."""
    logger.info("Received request at '/'")
    return web.Response(text="Hello, World!")


async def handle_slow(request: web.Request) -> web.Response:
    """Handles requests to the "/slow" route with a simulated delay."""
    logger.info("Received request at '/slow', simulating delay...")
    await asyncio.sleep(5)
    logger.info("Completed slow task.")
    return web.Response(text="Operation completed")


async def create_app() -> web.Application:
    """Creates and configures an aiohttp web application."""
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/slow", handle_slow)
    return app


async def run_server() -> None:
    """Runs the web server and shuts it down after test script execution."""
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="127.0.0.1", port=7777)
    await site.start()

    logger.info("Server started on http://127.0.0.1:7777")

    test_file = select_test_file()
    if test_file:
        logger.info(f"Running test script: {test_file}")
        subprocess.run([sys.executable, test_file])

    await asyncio.sleep(3)

    logger.info("Shutting down server...")
    await runner.cleanup()


def select_test_file() -> str | None:
    """Allows the user to select a test script before server starts."""
    test_folder = os.getcwd()
    print(f"Select a test script from {test_folder}:")

    test_files = [f for f in os.listdir(test_folder) if f.endswith(".py") and f != "async_web_server.py"]

    if not test_files:
        print("No test scripts found in the directory.")
        return None

    for i, file in enumerate(test_files, start=1):
        print(f"{i}: {file}")

    try:
        choice = int(input("Enter the number of the test script: ")) - 1
        if choice < 0 or choice >= len(test_files):
            raise ValueError
    except ValueError:
        print("Invalid selection.")
        return None

    return os.path.join(test_folder, test_files[choice])


if __name__ == "__main__":
    asyncio.run(run_server())
