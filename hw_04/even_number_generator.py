import os
from typing import Iterator


def even_number_generator() -> Iterator[int]:
    """
    Infinite generator that yields even numbers starting from 2.

    Yields:
        int: The next even number.
    """
    num: int = 2
    while True:
        yield num
        num += 2


class EvenNumberSaver:
    """
    Context manager that writes a limited number of even numbers to a file.
    """

    def __init__(self, file_name: str, limit: int = 100) -> None:
        """
        Initializes the context manager.

        Args:
            file_name (str): The name of the output file.
            limit (int): The number of even numbers to save. Defaults to 100.
        """
        self.file_name: str = file_name
        self.limit: int = limit

    def __enter__(self) -> None:
        """
        Enters the context and writes even numbers to the file.
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            generator = even_number_generator()
            for _ in range(self.limit):
                file.write(f"{next(generator)}\n")

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits the context. No special cleanup is required.
        """
        pass


def get_output_file_path() -> str:
    """
    Prompts the user to input the folder path for the output file.

    Returns:
        str: The path to the output file.
    """
    default_path: str = os.getcwd()
    user_input: str = input(f"Enter the folder path for output file (default: {default_path}): ").strip()
    folder_path: str = user_input or default_path
    return os.path.join(folder_path, "even_numbers.txt")


if __name__ == "__main__":
    output_file_path: str = get_output_file_path()

    with EvenNumberSaver(output_file_path):
        print(f"The first 100 even numbers have been saved to {output_file_path}.")
