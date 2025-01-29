import os
import csv
from typing import Iterator
from PIL import Image


class FolderImgIterator:
    """
    Iterator for iterating over files in a given directory with specified file extensions.
    """

    def __init__(self, folderPath: str, file_ext: list[str] = ['.jpg']) -> None:
        """
        Initializes the iterator.

        Args:
            folderPath (str): The path to the folder to iterate over.
            file_ext (list[str]): The file extensions to filter images (e.g., ['.jpg', '.png']). Defaults to ['.jpg'].

        Raises:
            ValueError: If the provided path is not a valid folder.
        """
        if not os.path.isdir(folderPath):
            raise ValueError(f"The path '{folderPath}' is not a valid directory.")

        self.folderPath: str = folderPath
        self.file_ext: list[str] = [ext.lower() for ext in file_ext]
        self.files: list[str] = os.listdir(folderPath)
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
        Returns the next file's metadata (name, size, format) for image files.

        Returns:
            dict: A dictionary contains the file's name, size, width, height, format, and mode.

        Raises:
            StopIteration: If there are no more files to iterate.
        """
        while self.index < len(self.files):
            file_name = self.files[self.index]
            file_path = os.path.join(self.folderPath, file_name)
            self.index += 1

            if os.path.isfile(file_path) and any(file_name.lower().endswith(ext) for ext in self.file_ext):
                try:
                    with Image.open(file_path) as image:  # Using 'with' to automatically close the image
                        metadata = {
                            'filename': file_name,
                            'width': image.width,
                            'height': image.height,
                            'format': image.format,
                            'mode': image.mode
                        }
                        return metadata
                except Exception as e:
                    return f"Error processing image '{file_name}': {e}"
        raise StopIteration


def get_directory_from_user() -> str:
    """
    Prompts the user to input a folder path.

    Returns:
        str: The chosen folder path.
    """
    default_path = os.getcwd()
    user_input = input(f"Enter the folder path (default: {default_path}): ").strip()
    return user_input if user_input else default_path


def save_metadata_to_csv(folderPath: str, output_csv: str, file_ext: list[str] = ['.jpg']) -> None:
    """
    Saves image metadata from all images in the folder to a CSV file.

    Args:
        folderPath (str): The folder containing image files.
        output_csv (str): The path to the output CSV file.
        file_ext (list[str]): The file extensions to filter images. Defaults to ['.jpg'].
    """
    iterator = FolderImgIterator(folderPath, file_ext)

    # Open the CSV file for writing
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['filename', 'width', 'height', 'format', 'mode']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write image metadata to CSV
        for img_metadata in iterator:
            writer.writerow(img_metadata)



folderPath = get_directory_from_user()  # Get the folder path from the user
file_ext = input("Enter img extensions separated by commas (like '.jpg,.png') or tap enter for default '.jpg': ").strip()

if file_ext:
    file_ext = [ext.strip() for ext in file_ext.split(',')]
else:
    file_ext = ['.jpg']

output_csv_filename = 'image_metadata.csv'
output_csv_path = os.path.join(folderPath, output_csv_filename)

save_metadata_to_csv(folderPath, output_csv_path, file_ext)
