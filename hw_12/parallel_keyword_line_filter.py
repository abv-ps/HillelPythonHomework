"""
This module provides efficient processing of large log files by filtering lines
that contain a specified keyword. It leverages concurrent threading to process
multiple log files in parallel, improving performance for large datasets.

Key features:
- Filters lines containing a given keyword (case-insensitive) from large log files.
- Supports concurrent processing of multiple log files using threads.
- Provides an interactive interface for selecting log files, specifying the keyword,
  and choosing the output directory.
- Saves filtered lines, including the line number of each match, to new files.

Classes:
- KeywordLineFilter: A generator that reads a large log file line by line and filters
  lines containing the specified keyword.

Functions:
- save_filtered_lines: Filters lines from an input file and writes them to an output file.
- get_user_input: Collects user input for paths, files, and keywords, with default values.
- get_file_from_directory: Prompts the user to select log files, output directory, and keyword.
- process_file: Filters a single log file in a separate thread and saves the results.
- process_files_concurrently: Processes multiple log files concurrently using threads.

Usage:
1. The user is prompted to provide a folder path containing log files, select the files,
   and specify a keyword for filtering.
2. The module processes the selected files concurrently, saving the filtered results
   to new files in the specified output directory.
"""

import os
import re
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator

from error_handler import handle_file_error
from logger_config import get_logger

logger = get_logger(__name__, "parallel_keyword_line_filter.log")


class KeywordLineFilter:
    """
    Generator for reading a large text file line by line and filtering lines
    containing a specific keyword, while also providing the line number.
    """

    def __init__(self, file_name: str, keyword: str, encoding: str = 'utf-8') -> None:
        """
        Initializes the generator.

        Args:
            file_name (str): The path to the file.
            keyword (str): The keyword to filter lines.
            encoding (str): The file encoding. Defaults to 'utf-8'.
        """
        self.file_name: str = file_name
        self.keyword: str = keyword
        self.encoding: str = encoding

    def __iter__(self) -> Iterator[str]:
        """
        Reads the file line by line and yields only lines containing the keyword
        along with their line number.

        Yields:
            str: The filtered lines containing the keyword with line numbers.
        """
        try:
            with open(self.file_name, 'r', encoding=self.encoding, errors='replace') as file:
                for line_number, line in enumerate(file, start=1):
                    if re.search(self.keyword, line, re.IGNORECASE):
                        yield f"Line {line_number}: {line.strip()}"
        except Exception as e:
            handle_file_error("read", self.file_name, e)
            raise


def save_filtered_lines(input_file: str, output_file: str, keyword: str = 'Error') -> None:
    """
    Reads a file, filters lines containing a specific keyword, and writes them to a new file.

    Args:
        input_file (str): The path to the input file.
        output_file (str): The path to the output file.
        keyword (str): The keyword to filter lines.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            for line in KeywordLineFilter(input_file, keyword):
                output.write(line + '\n')
    except Exception as e:
        handle_file_error("save", input_file, e)


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
        logger.info("Process interrupted by the user. Exiting...")
        sys.exit(0)


def get_file_from_directory() -> tuple[list[str], str, str]:
    """
    Prompts the user to input a folder path, lists log files, and allows selecting multiple files
    by entering their indexes, separated by commas.

    Returns:
        tuple[list[str], str, str]: A tuple containing a list of selected file paths,
                                    output file path, and search keyword.
    """
    default_path = os.path.join(os.getcwd(), "log_for_test")
    log_directory = get_user_input("Enter the folder path for log files", default_path)
    if not os.path.isdir(log_directory):
        logger.error("Invalid directory path.")
        sys.exit(0)

    log_files = [f for f in os.listdir(log_directory) if f.endswith(".log")]

    if not log_files:
        logger.error("No log files found in the selected directory.")
        sys.exit(0)

    print("Available log files:")
    for i, file in enumerate(log_files, start=1):
        print(f"{i}: {file}")

    file_indexes = get_user_input("Enter the numbers of the log files "
                                  "you want to analyze, separated by commas", "")
    try:
        selected_indexes = [int(index.strip()) - 1
                            for index in file_indexes.split(',')]  # Parse the indexes
        if any(index < 0 or index >= len(log_files) for index in selected_indexes):
            raise ValueError
    except ValueError:
        logger.error("Invalid selection.")
        sys.exit()

    input_file_paths = [os.path.join(log_directory, log_files[index])
                        for index in selected_indexes]
    output_directory = get_user_input("Enter the folder path for the output file",
                                      default_path)

    if not os.path.isdir(output_directory):
        logger.error("Invalid output directory.")
        sys.exit()

    search_keyword = get_user_input("Enter the keyword to search for", "Error")
    output_file_path = os.path.join(output_directory, f"filtered_{search_keyword}.txt")

    return input_file_paths, output_file_path, search_keyword


def process_file(input_file_path: str, output_file_path: str, keyword: str) -> None:
    """
    Processes a single file to filter lines containing the keyword in a separate thread.
    Args:
        input_file_path (str): The input file path.
        output_file_path (str): The output file path.
        keyword (str): The keyword to search for.
    """
    logger.info("Processing file: %s", input_file_path)
    save_filtered_lines(input_file_path, output_file_path, keyword)
    logger.info("Finished processing file: %s", input_file_path)


def process_files_concurrently(file_paths: list, output_directory: str,
                               keyword: str) -> None:
    """
    Processes multiple log files concurrently to filter lines containing the keyword.

    Args:
        file_paths (list): A list of input file paths to process.
        output_directory (str): The output directory for filtered results.
        keyword (str): The keyword to filter lines.
    """
    with ThreadPoolExecutor() as executor:
        executor.map(lambda file_path: process_file(file_path,
                                    os.path.join(output_directory,
                                                 f"filtered_{os.path.basename(file_path)}"),
                                    keyword),
                     file_paths)

def signal_handler(signum, frame):
    """
    Обробник сигналу для SIGINT (Ctrl+C).
    """
    logger.info("\nProcess interrupted by the user. Exiting gracefully...")
    sys.exit(0)

def main():
    """
    The main function of the program that orchestrates the file processing.

    This function performs the following steps:
    1. Retrieves the folder paths (input and output file paths and the search keyword)
       from the `get_file_from_directory()` function.
    2. Extracts the input file paths, output file path, and search keyword
       from the retrieved folder paths.
    3. Determines the directory of the output file path.
    4. Calls `process_files_concurrently()` to process the input files in parallel,
       searching for the specified keyword and saving the results to the output directory.
    5. Prints a message indicating that the filtered lines containing the search keyword
       have been saved to the corresponding output files.

    Returns:
    None
    """
    try:
        signal.signal(signal.SIGINT, signal_handler)
        folder_paths = get_file_from_directory()
        input_file_paths = folder_paths[0]
        output_file_path = folder_paths[1]
        search_keyword = folder_paths[2]

        output_directory = os.path.dirname(output_file_path)

        process_files_concurrently(input_file_paths, output_directory, search_keyword)

        logger.info("Filtered lines containing '%s' have been saved "
                "to corresponding output files.", search_keyword)
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by the user. Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
