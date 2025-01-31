import os
import re
from typing import Iterator, List


class KeywordLineFilter:
    """
    Generator for reading a large text file line by line and filtering lines containing a specific keyword,
    while also providing the line number.
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
        Reads the file line by line and yields only lines containing the keyword along with their line number.

        Yields:
            str: The filtered lines containing the keyword with line numbers.
        """
        with open(self.file_name, 'r', encoding=self.encoding, errors='replace') as file:
            for line_number, line in enumerate(file, start=1):  # Start line numbering from 1
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


def get_file_from_directory() -> tuple[str, str, str]:
    """
    Prompts the user to input a folder path, lists log files, and allows selecting one.

    Returns:
        tuple[str, str, str]: A tuple containing the selected file path, output file path, and search keyword.
    """
    default_path = os.getcwd()
    user_input_log = input(f"Enter the folder path for log files (default: {default_path}): ").strip()
    log_directory = user_input_log if user_input_log else default_path

    if not os.path.isdir(log_directory):
        print("Invalid directory path.")
        exit()

    log_files = [f for f in os.listdir(log_directory) if f.endswith(".log")]

    if not log_files:
        print("No log files found in the selected directory.")
        exit()

    print("Available log files:")
    for i, file in enumerate(log_files, start=1):
        print(f"{i}: {file}")

    try:
        file_index = int(input("Enter the number of the log file you want to analyze: ")) - 1
        if file_index < 0 or file_index >= len(log_files):
            raise ValueError
    except ValueError:
        print("Invalid selection.")
        exit()

    input_file_path = os.path.join(log_directory, log_files[file_index])

    user_input_out = input(f"Enter the folder path for output file (default: {default_path}): ").strip()
    output_directory = user_input_out or default_path

    if not os.path.isdir(output_directory):
        print("Invalid output directory.")
        exit()

    search_keyword = input("Enter the keyword to search for (default: 'Error'): ").strip() or "Error"
    output_file_path = os.path.join(output_directory, f"filtered_{search_keyword}.txt")

    return input_file_path, output_file_path, search_keyword


if __name__ == "__main__":
    folder_paths = get_file_from_directory()
    input_file_path = folder_paths[0]
    output_file_path = folder_paths[1]
    search_keyword = folder_paths[2]

    save_filtered_lines(input_file_path, output_file_path, search_keyword)

    print(f"Filtered lines containing '{search_keyword}' have been saved to: {output_file_path}")
