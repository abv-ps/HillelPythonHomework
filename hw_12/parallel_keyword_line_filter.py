"""
This module provides functionality for processing large log files, filtering lines
that contain a specific keyword, and saving the filtered lines to new files.
The processing is done concurrently using threads for improved performance.

Key features of the module:
- Filters lines containing a specified keyword (case-insensitive) from large log files.
- Processes multiple log files concurrently using threads.
- Allows the user to interactively select log files, specify the keyword,
  and choose the output directory.
- Saves the filtered lines to a new file, including the line number of each matching line.

Classes:
- KeywordLineFilter: A generator class that reads a large text file line by line
  and filters lines that contain a specified keyword.

Functions:
- save_filtered_lines: Reads a file, filters lines containing the specified keyword,
  and writes them to a new file.
- get_file_from_directory: Prompts the user to select log files, output directory,
  and keyword for filtering.
- process_file: Processes an individual file to filter lines containing
  the keyword using a separate thread.
- process_files_concurrently: Processes multiple log files concurrently using threads.

Usage:
1. The user is prompted to input a folder path containing log files, select the files,
   and specify a keyword for filtering.
2. The selected files are processed concurrently, with filtered lines being saved
   to new files in the specified output directory.
"""

import os
import re
import sys
import threading
from typing import Iterator


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
        with open(self.file_name, 'r', encoding=self.encoding, errors='replace') as file:
            for line_number, line in enumerate(file, start=1):
                if re.search(self.keyword, line, re.IGNORECASE):
                    yield f"Line {line_number}: {line.strip()}"


def save_filtered_lines(input_file: str, output_file: str, keyword: str = 'Error') -> None:
    """
    Reads a file, filters lines containing a specific keyword, and writes them to a new file.

    Args:
        input_file (str): The path to the input file.
        output_file (str): The path to the output file.
        keyword (str): The keyword to filter lines.
    """
    with open(output_file, 'w', encoding='utf-8') as output:
        for line in KeywordLineFilter(input_file, keyword):
            output.write(line + '\n')


def get_file_from_directory() -> tuple[list[str], str, str]:
    """
    Prompts the user to input a folder path, lists log files, and allows selecting multiple files
    by entering their indexes, separated by commas.

    Returns:
        tuple[list[str], str, str]: A tuple containing a list of selected file paths,
                                    output file path, and search keyword.
    """
    default_path = os.path.join(os.getcwd(), "log_for_test")
    user_input_log = input(f"Enter the folder path for log files "
                           f"(default: {default_path}): ").strip()
    log_directory = user_input_log if user_input_log else default_path

    if not os.path.isdir(log_directory):
        print("Invalid directory path.")
        sys.exit()

    log_files = [f for f in os.listdir(log_directory) if f.endswith(".log")]

    if not log_files:
        print("No log files found in the selected directory.")
        sys.exit()

    print("Available log files:")
    for i, file in enumerate(log_files, start=1):
        print(f"{i}: {file}")

    try:
        file_indexes = input("Enter the numbers of the log files you want to analyze, "
                             "separated by commas: ")
        selected_indexes = [int(index.strip()) - 1
                            for index in file_indexes.split(',')]  # Parse the indexes
        if any(index < 0 or index >= len(log_files) for index in selected_indexes):
            raise ValueError
    except ValueError:
        print("Invalid selection.")
        sys.exit()

    input_file_paths = [os.path.join(log_directory, log_files[index])
                        for index in selected_indexes]

    user_input_out = input(f"Enter the folder path for the output file "
                           f"(default: {default_path}): ").strip()
    output_directory = user_input_out or default_path

    if not os.path.isdir(output_directory):
        print("Invalid output directory.")
        sys.exit()

    search_keyword = input("Enter the keyword to search for "
                           "(default: 'Error'): ").strip() or "Error"
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
    print(f"Processing file: {input_file_path}")
    save_filtered_lines(input_file_path, output_file_path, keyword)
    print(f"Finished processing file: {input_file_path}")


def process_files_concurrently(file_paths: list, output_directory: str,
                               keyword: str) -> None:
    """
    Processes multiple log files concurrently to filter lines containing the keyword.

    Args:
        file_paths (list): A list of input file paths to process.
        output_directory (str): The output directory for filtered results.
        keyword (str): The keyword to filter lines.
    """
    threads = []
    for file_path in file_paths:
        output_file_path = os.path.join(output_directory, f"filtered_{os.path.basename(file_path)}")
        thread = threading.Thread(target=process_file, args=(file_path, output_file_path, keyword))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


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
    folder_paths = get_file_from_directory()
    input_file_paths = folder_paths[0]
    output_file_path = folder_paths[1]
    search_keyword = folder_paths[2]

    output_directory = os.path.dirname(output_file_path)

    process_files_concurrently(input_file_paths, output_directory, search_keyword)

    print(f"Filtered lines containing '{search_keyword}' have been saved "
          f"to corresponding output files.")


if __name__ == "__main__":
    main()
