"""
This module allows the user to select a Python file from a specified directory
and choose an action to perform on that file. The available actions include
running `mypy`, `pyright`, or `pylint` on the selected file. The module provides
functions to handle user input, check file existence, and run the appropriate
tool based on user selection.

The `get_user_input` function handles user input with an option to use a default
value and gracefully handles `KeyboardInterrupt` to exit the program.

Dependencies:
    - subprocess: To run external commands (`mypy`, `pyright`, `pylint`) on the
      selected file.
    - os: For interacting with the file system (checking file existence,
      handling directories).
    - sys: For exiting the program in case of errors or interruptions.
    - logging: For logging interruptions and errors.

Key Components:
    1. `get_user_input` Function:
        Args:
            prompt (str): The message shown to the user.
            default (str): The default value if the user presses Enter without input.

        Returns:
            str: The user's input or the default value.

    2. `run_linter_or_type_check` Function:
        Args:
            file_name (str): The file to run the tool on.

        Description:
            This function asks the user what action they want to perform on the
            file, validates the file existence, and then runs the appropriate tool
            (`mypy`, `pyright`, or `pylint`) using the `subprocess` module.

    3. `choose_file_and_action` Function:
        Description:
            This function allows the user to select a Python file from a directory
            and choose an action to perform on the selected file.

    4. Logging:
        The module uses a logger to log interruptions and errors. If the user
        interrupts the program or if an error occurs, the program logs the event
        and exits gracefully.

Usage:
    This module can be executed in a terminal. It will prompt the user to select
    a file and an action to run on that file. The selected file will be processed
    using the chosen tool.
"""

import os
import sys
import subprocess
from logger_config import get_logger

# Set up logger for handling logs
logger = get_logger(__name__, "run_check.log")


def get_user_input(prompt: str, default: str) -> str:
    """
    A helper function to get user input with handling for KeyboardInterrupt.

    Args:
        prompt (str): The prompt message to display.
        default (str): The default value to use if the user does not input anything.

    Returns:
        str: The user input, or the default value if the user pressed Enter without input.
    """
    try:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    except KeyboardInterrupt:
        logger.error("Process interrupted by the user. Exiting...")
        sys.exit(0)


def run_linter_or_type_check(file_name):
    """
    Prompts the user to choose a linter or type checker to run on the specified file.
    The available options are `mypy`, `pyright`, and `pylint`, each mapped to a numeric input
    (1 for `mypy`, 2 for `pyright`, and 3 for `pylint`). The function checks if the file exists,
    and then executes the selected tool on the file.

    Args:
        file_name (str): The path to the Python file to be checked.

    Exits:
        The function exits the program if the specified file does not exist, if the user selects
        an invalid option, or if an error occurs while running the selected tool.

    Logs:
        Logs error messages if the file does not exist, if an invalid choice is made, or if
        an error occurs while running the command. Logs an informational message when a tool is
        successfully executed on the file.
    """
    action = get_user_input("What do you want to do with the file? "
                            "(1: mypy, 2: pyright, 3: pylint)", "1")

    if not os.path.isfile(file_name):
        logger.error("Error: %s does not exist.", file_name)
        sys.exit(1)

    action_map = {
        "1": ["mypy", file_name],
        "2": ["pyright", file_name],
        "3": ["pylint", file_name],
    }
    command = action_map.get(action)

    if command is None:
        logger.error("Invalid choice. Please select 1 for 'mypy', "
                     "2 for 'pyright', or 3 for 'pylint'.")
        sys.exit(1)

    try:
        logger.warning("Running %s on %s...", action, file_name)
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Error occurred while running %s on %s: %s",
                     action, file_name, str(e))
        sys.exit(1)


def choose_file_and_action():
    """
    Prompts the user to choose a directory containing Python files and then select
    one Python file from the directory to run a linter or type checker on.

    The function lists all `.py` files in the specified directory, asks the user to
    select one of the files, and then calls the `run_linter_or_type_check` function
    to perform the selected action (`mypy`, `pyright`, or `pylint`) on the chosen file.

    Exits:
        The function exits the program if the directory path is invalid, if no `.py`
        files are found in the directory, if the user makes an invalid file selection,
        or if any other error occurs during execution.

    Logs:
        Logs error messages if the directory path is invalid, if no Python files are
        found, if the user makes an invalid selection, or if any unexpected issue occurs.
        Logs the list of available Python files and the file selected by the user.
    """
    #default_path = os.getcwd()
    #check_directory = get_user_input("Enter the folder path for files to check", default_path)
    check_directory = os.getcwd()
    if not os.path.isdir(check_directory):
        logger.error("Invalid directory path: %s", check_directory)
        sys.exit(0)

    check_files = [f for f in os.listdir(check_directory) if f.endswith(".py")]

    if not check_files:
        logger.error("No .py files found in the selected directory.")
        sys.exit(0)

    logger.warning("Available .py files:")
    for i, file in enumerate(check_files, start=1):
        logger.warning("%d: %s", i, file)

    file_indexes = get_user_input("Enter the number of the .py file you want to select", "")
    try:
        selected_index = int(file_indexes.strip()) - 1  # Parse the selected index
        if selected_index < 0 or selected_index >= len(check_files):
            raise ValueError
    except ValueError:
        logger.error("Invalid selection.")
        sys.exit(0)

    selected_file = os.path.join(check_directory, check_files[selected_index])

    run_linter_or_type_check(selected_file)

def main():
    """
    The main entry point of the program. This function is executed when the script is run directly.

    It calls the `choose_file_and_action` function, which prompts the user to select a Python file
    from a specified directory and then run a linter or type checker
    (`mypy`, `pyright`, or `pylint`) on the selected file.

    This function is invoked when the script is executed as the main program
    (i.e., not imported as a module).
    """
    try:
        choose_file_and_action()
    except KeyboardInterrupt:
        logger.error("Process interrupted by the user. Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
