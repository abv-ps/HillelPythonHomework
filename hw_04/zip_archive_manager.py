import os
import zipfile
from typing import Optional, List
from datetime import datetime

def get_file_for_zip() -> List[str]:
    """
    Prompts the user to input a folder path, lists available files, and allows selecting one.
    Also prompts for an output directory for the ZIP archive.

    Returns:
        List[str]: A list containing the selected file path and the output ZIP archive path.
    """
    default_path: str = os.getcwd()
    user_input_dir: str = input(
        f"Enter the folder path containing files to archive (default: {default_path}): ").strip()
    file_directory: str = user_input_dir or default_path

    if not os.path.isdir(file_directory):
        print("Error: Invalid directory path.")
        exit()

    available_files: List[str] = [f for f in os.listdir(file_directory) if
                                  os.path.isfile(os.path.join(file_directory, f))]

    if not available_files:
        print("Error: No files found in the selected directory.")
        exit()

    print("Available files:")
    for i, file in enumerate(available_files, start=1):
        print(f"{i}: {file}")

    try:
        file_index: int = int(input("Enter the number of the file you want to archive: ")) - 1
        if file_index < 0 or file_index >= len(available_files):
            raise ValueError
    except ValueError:
        print("Error: Invalid selection.")
        exit()

    input_file_path: str = os.path.join(file_directory, available_files[file_index])

    user_input_out: str = input(f"Enter the folder path to save the ZIP archive (default: {default_path}): ").strip()
    output_directory: str = user_input_out or default_path

    if not os.path.isdir(output_directory):
        print("Error: Invalid output directory.")
        exit()

    # Get current date/time for timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
    file_name = os.path.splitext(available_files[file_index])[0]  # Get the original file name without extension
    zip_file_name = f"{file_name}_{timestamp}.zip"  # Add timestamp to the file name
    zip_file_path: str = os.path.join(output_directory, zip_file_name)

    return [input_file_path, zip_file_path]


class ZipArchiveManager:
    """
    Context manager that adds files to a ZIP archive, ensuring the archive is properly closed when exiting the context.
    """

    def __init__(self, zip_name: str) -> None:
        """
        Initializes the ZIP archive manager.

        Args:
            zip_name (str): The name of the ZIP archive to be created.
        """
        self.zip_name = zip_name
        self.zip_file = None

    def __enter__(self) -> "ZipArchiveManager":
        """
        Opens the ZIP archive for writing.

        Returns:
            ZipArchiveManager: The instance of the context manager.
        """
        self.zip_file = zipfile.ZipFile(self.zip_name, 'w', zipfile.ZIP_DEFLATED)
        return self

    def add_file(self, file_path: str) -> None:
        """
        Adds a file to the ZIP archive.

        Args:
            file_path (str): The path to the file to be added.
        """
        if self.zip_file is None:
            raise RuntimeError("ZIP archive is not open.")

        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.zip_file.write(file_path, os.path.split(file_path)[1])  # Add the file to the archive
        else:
            print(f"Warning: File '{file_path}' does not exist or is not a file.")

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[object]) -> None:
        """
        Closes the ZIP archive upon exiting the context.
        """
        if self.zip_file:
            self.zip_file.close()
            print(f"ZIP archive '{self.zip_name}' has been created successfully.")


if __name__ == "__main__":
    input_file, zip_output = get_file_for_zip()

    with ZipArchiveManager(zip_output) as archive:
        archive.add_file(input_file)
