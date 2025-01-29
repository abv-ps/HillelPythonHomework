import os
from typing import Iterator
from datetime import datetime


class DirectoryFilesIterator:
    """
    Iterator for iterating over files in a given directory.
    """

    def __init__(self, directory_path: str) -> None:
        """
        Initializes the iterator.

        Args:
            directory_path (str): The path to the directory to iterate over.

        Raises:
            ValueError: If the provided path is not a valid directory.
        """
        if not os.path.isdir(directory_path):
            raise ValueError(f"The path '{directory_path}' is not a valid directory.")

        self.directory_path: str = directory_path
        self.files: list[str] = os.listdir(directory_path)
        self.index: int = 0

    def __iter__(self) -> Iterator[str]:
        """
        Returns the iterator object.

        Returns:
            Iterator[str]: The iterator itself.
        """
        return self

    def __next__(self) -> str:
        """
        Returns the next file's information (name, size, and last modified date).

        Returns:
            str: A string containing the file's name, size, and last modified date.

        Raises:
            StopIteration: If there are no more files to iterate over.
        """
        while self.index < len(self.files):
            file_name = self.files[self.index]
            file_path = os.path.join(self.directory_path, file_name)
            self.index += 1

            if os.path.isfile(file_path):  # Check if it's a file
                try:
                    file_size = os.path.getsize(file_path)
                    last_modified_time = os.path.getmtime(file_path)
                    last_modified_date = datetime.fromtimestamp(last_modified_time).isoformat()

                    # Prepare the string with file info
                    return f"Name: {file_name}, Size: {file_size} bytes, Last modified: {last_modified_date}"
                except (FileNotFoundError, PermissionError) as e:
                    return f"Error accessing file '{file_name}': {e}"
            else:
                return f"Name: {file_name} (Not a file)"

        raise StopIteration


def get_directory_from_user() -> str:
    """
    Prompts the user to input a directory path.

    Returns:
        str: The chosen directory path.
    """
    default_path = os.getcwd()
    user_input = input(f"Enter the directory path (default: {default_path}): ").strip()
    return user_input if user_input else default_path


if __name__ == "__main__":
    directory_path = get_directory_from_user()

    try:
        directory_iterator = DirectoryFilesIterator(directory_path)
        for file_info in directory_iterator:
            print(file_info)
    except ValueError as e:
        print(f"Error: {e}")
