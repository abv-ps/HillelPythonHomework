"""
This module provides a function that prompts the user for input
with a specified time limit. If the user doesn't respond within
the given time, the function returns None and prints a timeout message.
It uses Python's threading module to handle the input and timeout mechanism simultaneously.

Key features:

User input is captured through a prompt, and a timeout is applied.
The input is processed in a separate thread, allowing for concurrent waiting for input and checking for a timeout.
If the user provides input within the given time, it is returned; otherwise, a timeout message is displayed.
"""

import threading
import time
from typing import Optional


def input_with_timeout(prompt: str, timeout: int = 5) -> Optional[str]:
    """
    Prompts the user for input with a time limit.

    Uses threading to wait for input and a timeout mechanism.

    Args:
        prompt (str): The message to display to the user.
        timeout (int): The time limit (in seconds) for user input.

    Returns:
        Optional[str]: The input entered by the user, or None if the input times out.

    Example:
        >>> input_with_timeout("Enter something: ", 5)
        Enter something: (User input or 'Time is up!' message)
    """

    def timed_input(result: list) -> None:
        """Helper function to capture input within a timeout."""
        result.append(input(prompt))

    # Create a list to store the result of input
    result: list = []

    # Start a thread to prompt the user for input
    input_thread = threading.Thread(target=timed_input, args=(result,))
    input_thread.start()

    # Wait for the input thread to finish or for the timeout to occur
    input_thread.join(timeout)

    if result:
        return result[0]  # User provided input
    else:
        print("Time is up!")
        return None  # Timeout occurred


# Example usage
if __name__ == "__main__":
    user_input = input_with_timeout("Enter something: ", 5)
    if user_input:
        print(f"You entered: {user_input}")
    else:
        print("No input received.")
