import os, re
from typing import Iterator, List


class KeywordLineFilter:
    """
    Generator for reading a large text file line by line and filtering lines containing a specific keyword.
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
        Reads the file line by line and yields only lines containing the keyword.

        Yields:
            str: The filtered lines containing the keyword.
        """
        with open(self.file_name, 'r', encoding=self.encoding, errors='replace') as file:
            for line in file:
                if re.search(self.keyword, line, re.IGNORECASE):
                    yield line.strip()


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


def get_directory_from_user() -> List[str]:
    """
    Prompts the user to input folder paths for both the log file and the output file.

    Returns:
        List[str]: A list containing two folder paths: one for the log file and one for the output file.
    """
    default_path: str = os.getcwd()
    user_input_log: str = input(f"Enter the folder path for log file (default: {default_path}): ").strip()
    user_input_out: str = input(f"Enter the folder path for output file (default: {default_path}): ").strip()
    folder_list: List[str] = [
        user_input_log or default_path,
        user_input_out or default_path
    ]
    return folder_list


folder_path: List[str] = get_directory_from_user()
input_file_path: str = folder_path[0]
output_file_path: str = folder_path[1]
search_keyword: str = input("Enter the keyword to search for (default: 'Error'): ").strip()

if not search_keyword:
    search_keyword = "Error"

save_filtered_lines(input_file_path, output_file_path, search_keyword)
