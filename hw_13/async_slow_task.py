"""
This module demonstrates how to use asyncio to manage asynchronous tasks
and handle timeouts using asyncio.wait_for.

The module defines two functions:
    - slow_task: Simulates a task that takes 10 seconds to complete.
    - main: Runs the slow_task with a timeout of 5 seconds using asyncio.wait_for().

Usage:
    The main function is executed when the module is run directly, and it demonstrates
    how to handle a timeout using asyncio.
"""
import asyncio

async def slow_task() -> None:
    """
    Simulates a task that takes 10 seconds to complete.

    This function uses asyncio.sleep() to simulate a long-running task that
    takes 10 seconds. It prints a start message, waits for 10 seconds, and
    then prints a completion message.

    Returns:
        None: This function does not return any value.
    """
    print("Starting slow task...")
    await asyncio.sleep(10)  # Simulates a task that takes 10 seconds
    print("Slow task completed.")


async def main() -> None:
    """
    Runs the slow_task with a timeout of 5 seconds using asyncio.wait_for().

    The main function attempts to execute the slow_task, but with a timeout of 5 seconds.
    If the task does not complete within the timeout period, a TimeoutError is raised,
    and a message is printed to the console indicating the timeout was exceeded.

    Returns:
        None: This function does not return any value.
    """
    try:
        # Use asyncio.wait_for to apply a timeout to slow_task
        await asyncio.wait_for(slow_task(), timeout=5)
    except asyncio.TimeoutError:
        print("Timeout exceeded while waiting for the task to complete.")


if __name__ == "__main__":
    asyncio.run(main())
