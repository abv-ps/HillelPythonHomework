import os
from datetime import datetime


def write_log(message: str) -> None:
    """
    Logs a message to a file with a timestamp.

    Args:
        message (str): The message to log.

    Returns:
        None
    """
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"log_{current_time}.log"

    # Define the log file path
    log_path = os.path.join(os.path.dirname(__file__), log_filename)

    # Write the message to the log file
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{current_time} - {message}\n")


write_log("Package 'my_package' imported.")