import signal


# Function to handle timeout exception
def timeout_handler(signum: int, frame: signal.FrameType) -> None:
    """
    This function is called when the input times out.
    It raises a TimeoutError with a custom message.

    Args:
        signum (int): Signal number that caused the handler to be invoked.
        frame (signal.FrameType): Current stack frame when the signal was received.
    """
    raise TimeoutError("Input timed out!")


# Set the signal handler to limit input time
signal.signal(signal.SIGALRM, timeout_handler)


def input_with_timeout(prompt: str, timeout: int = 5) -> str | None:
    """
    Prompts the user for input with a specified time limit.

    Args:
        prompt (str): The message displayed to the user when requesting input.
        timeout (int, optional): The number of seconds to wait for input. Defaults to 5 seconds.

    Returns:
        str | None: The input entered by the user, or None if the input times out.

    Raises:
        TimeoutError: If the user does not provide input within the given time limit.

    Example:
        >>> user_input = input_with_timeout("Enter something: ", 3)
        >>> print(user_input)
        Enter something:  (if user enters within 3 seconds) or "Time is up!" message if times out
    """
    # Set the timer for input timeout
    signal.alarm(timeout)

    try:
        # Wait for user input
        return input(prompt)
    except TimeoutError:
        # If time is up, print the timeout message and return None
        print("Time is up! No input was provided.")
        return None
    finally:
        # Reset the signal after input or timeout
        signal.alarm(0)
