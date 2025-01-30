import os
import shutil
from typing import List, Optional
from datetime import datetime
import getpass

def get_file_from_directory() -> str:
    """
    Prompts the user to input a folder path, lists log files, and allows selecting one.

    Returns:
        str: The selected file path.
    """
    default_path: str = os.getcwd()
    user_input: str = input(f"Enter the folder path to select a file for processing (default: {default_path}): ").strip()
    processing_path: str = user_input or default_path

    if not os.path.isdir(processing_path):
        print("Error: Invalid directory path.")
        exit()

    processing_files: List[str] = [f for f in os.listdir(processing_path)]

    if not processing_files:
        print("Error: No files found in the selected directory.")
        exit()

    print("Available files to process:")
    for i, file in enumerate(processing_files, start=1):
        print(f"{i}: {file}")

    try:
        file_index: int = int(input("Enter the number of the file you want to process: ")) - 1
        if file_index < 0 or file_index >= len(processing_files):
            raise ValueError
    except ValueError:
        print("Error: Invalid selection.")
        exit()

    return os.path.join(processing_path, processing_files[file_index])


class FileBackupManager:
    """
    Context manager that creates a backup of an important file before processing it.
    If an error occurs during processing, the backup is restored automatically.
    If processing is successful, the original file is replaced with the new one.
    """
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        # Create a backup file name with current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.backup_path = f"{file_path}.{timestamp}.bak"
        self.temp_path = f"{file_path}.tmp"

    def __enter__(self) -> str:
        """
        Creates a backup of the original file.

        Returns:
            str: Path to the temporary file for processing.
        """
        if os.path.exists(self.file_path):
            shutil.copy2(self.file_path, self.backup_path)  # Backup with timestamped name
        shutil.copy2(self.file_path, self.temp_path)
        return self.temp_path

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[object]) -> None:
        """
        Handles exit from the processing context, ensuring proper cleanup or restoration if needed.
        If no exception occurs, replaces the original file with the processed one.
        If an exception occurs, restores the original file from the backup.
        """
        if exc_type is None:
            shutil.move(self.temp_path, self.file_path)
            # if os.path.exists(self.backup_path): # Do not remove the backup file, as it contains a unique timestamp
            #    os.remove(self.backup_path) # No deletion of backup file
        else:
            # Restore the original file from the backup if there was an exception
            if os.path.exists(self.backup_path):
                shutil.move(self.backup_path, self.file_path)
            if os.path.exists(self.temp_path):
                os.remove(self.temp_path)


def modification_file(file_path: str) -> None:
    """
    Allows the user to edit a file and saves changes upon confirmation.
    Adds timestamp and username as a comment at the end of the file.

    Args:
        file_path (str): The path to the file for modification.
    """
    # Get the current date/time and username
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_name = getpass.getuser()  # Get the current username

    with FileBackupManager(file_path) as temp_file:
        with open(temp_file, "r", encoding="utf-8") as t_f:
            some_data = t_f.read()

        print("Current file data:")
        print(some_data)

        new_data = input("Enter new information (if you want to change file): ").strip()
        if not new_data:
            print("No changes made. Exiting.")
            return

        confirm = input("Do you want to save changes? (1/0 or yes/no): ").strip().lower()
        if confirm in ["yes", "1"]:
            # Append the change log (timestamp and user) to the data
            change_log = f"\n\n# Change made on {timestamp} by {user_name}\n"
            new_data += change_log

            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(new_data)
            print("Changes saved successfully.")
        elif confirm in ["no", "0"]:
            print("Changes discarded.")
        else:
            print("Invalid input. Please enter 1, 0, yes, or no.")


if __name__ == "__main__":
    file_path = get_file_from_directory()
    modification_file(file_path)
