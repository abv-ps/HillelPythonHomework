import os
import re
from typing import Iterator, List


class StatusCodeLineFilter:
    """
    Generator for reading a large text file line by line and filtering lines containing
    HTTP error status codes (4XX or 5XX) with displaying the line number.
    """

    def __init__(self, file_name: str, encoding: str = "utf-8") -> None:
        """
        Initializes the generator.

        Args:
            file_name (str): The path to the file.
            encoding (str): The file encoding. Defaults to 'utf-8'.
        """
        self.file_name: str = file_name
        self.encoding: str = encoding

    def __iter__(self) -> Iterator[str]:
        """
        Reads the file line by line and yields only lines containing 4XX or 5XX status codes.

        Yields:
            str: Filtered lines containing 4XX or 5XX status codes with their line numbers.
        """
        status_code_pattern = re.compile(r"\s[45]\d{2}\s")
        try:
            with open(self.file_name, "r", encoding=self.encoding, errors="replace") as file:
                for line_number, line in enumerate(file, start=1):
                    if status_code_pattern.search(line):
                        yield f"Line {line_number}: {line.strip()}"
        except FileNotFoundError:
            print(f"Error: File '{self.file_name}' not found.")
        except Exception as e:
            print(f"Error reading file '{self.file_name}': {e}")


def save_filtered_lines(input_file: str, output_file: str) -> None:
    """
    Reads a file, filters lines containing HTTP status codes 4XX or 5XX,
    and writes them to a new file.

    Args:
        input_file (str): The path to the input file.
        output_file (str): The path to the output file.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as output:
            for line in StatusCodeLineFilter(input_file):
                output.write(line + "\n")
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}")


def get_file_from_directory() -> List[str]:
    """
    Prompts the user to input a folder path, lists log files, and allows selecting one.

    Returns:
        List[str]: A list containing the selected file path and the output file path.
    """
    default_path: str = os.getcwd()
    user_input_log: str = input(f"Enter the folder path for log files (default: {default_path}): ").strip()
    log_directory: str = user_input_log or default_path

    if not os.path.isdir(log_directory):
        print("Error: Invalid directory path.")
        exit()

    log_files: List[str] = [f for f in os.listdir(log_directory) if f.endswith(".log")]

    if not log_files:
        print("Error: No log files found in the selected directory.")
        exit()

    print("Available log files:")
    for i, file in enumerate(log_files, start=1):
        print(f"{i}: {file}")

    try:
        file_index: int = int(input("Enter the number of the log file you want to analyze: ")) - 1
        if file_index < 0 or file_index >= len(log_files):
            raise ValueError
    except ValueError:
        print("Error: Invalid selection.")
        exit()

    input_file_path: str = os.path.join(log_directory, log_files[file_index])

    user_input_out: str = input(f"Enter the folder path for output file (default: {default_path}): ").strip()
    output_directory: str = user_input_out or default_path

    if not os.path.isdir(output_directory):
        print("Error: Invalid output directory.")
        exit()

    output_file_path: str = os.path.join(output_directory, "filtered_status_errors.txt")

    return [input_file_path, output_file_path]


if __name__ == "__main__":
    folder_paths: List[str] = get_file_from_directory()
    input_file_path: str = folder_paths[0]
    output_file_path: str = folder_paths[1]

    save_filtered_lines(input_file_path, output_file_path)

    print(f"Filtered lines containing HTTP status codes 4XX or 5XX have been saved to: {output_file_path}")
