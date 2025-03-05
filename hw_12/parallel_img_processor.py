"""
Module for processing images by resizing them and saving to a specified output folder.

This module provides functions for resizing images and processing multiple images in parallel.

Functions:
    process_image(image_path: str, output_folder: str, size: tuple[int, int]) -> None:
        Resizes an image and saves it to the specified output folder.

    process_images_parallel(image_paths: list[str], output_folder: str, size: tuple[int, int],
                            max_workers: int = 4) -> None:
        Processes multiple images concurrently using a pool of worker processes.
"""

import os
from concurrent.futures import ProcessPoolExecutor
from PIL import Image


def process_image(image_path: str, output_folder: str, size: tuple[int, int]) -> None:
    """
    Resizes an image and saves it to the output folder.

    Args:
        image_path (str): Path to the input image.
        output_folder (str): Folder where processed images will be saved.
        size (tuple[int, int]): New size for the image.
    """
    try:
        img = Image.open(image_path)
        img_resized = img.resize(size)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_path = os.path.join(output_folder, os.path.basename(image_path))
        img_resized.save(output_path)
        print(f"Processed: {output_path}")
    except OSError as e:
        if isinstance(e, PermissionError):
            print(f"Permission error when accessing {image_path} or {output_folder}")
        elif isinstance(e, IsADirectoryError):
            print(f"The path {image_path} is a directory, not a file.")
        elif isinstance(e, FileNotFoundError):
            print(f"File not found: {image_path}")
        else:
            print(f"Unable to open or save the image: {image_path} - {e}")
    except ValueError:
        print(f"Invalid size for resizing: {size}")
    except TypeError:
        print(f"Invalid type for size: {size}")
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")


def process_images_parallel(image_paths: list[str], output_folder: str,
                            size: tuple[int, int], max_workers: int = 4) -> None:
    """
    Processes multiple images in parallel.

    Args:
        image_paths (list[str]): List of image file paths.
        output_folder (str): Folder where processed images will be saved.
        size (tuple[int, int]): New size for the images.
        max_workers (int): Number of worker processes to use.
    """
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_image, image_paths,
                     [output_folder] * len(image_paths), [size] * len(image_paths))

    print("All images processed.")


def main():
    """
    The main function of the program that processes a list of images in parallel.

    This function performs the following steps:
    1. Retrieves the current working directory using `os.getcwd()`.
    2. Defines a list of image file names (`input_images`).
    3. Creates a list of full file paths (`input_path`) by joining the current directory
       with each image file name.
    4. Prints the full paths of the input images.
    5. Defines the output directory (`output_directory`) where processed images will be saved.
    6. Defines the new size (`new_size`) to which the images will be resized.
    7. Calls the `process_images_parallel()` function to process the images concurrently,
       resizing them and saving them to the output directory.

    Returns:
    None
    """
    current_directory = os.getcwd()
    input_images = ["image1.jpg", "image2.jpg", "image3.jpg"]
    input_path = [os.path.join(current_directory, "img_for_test", file_name)
                  for file_name in input_images]
    for path in input_path:
        print(path)
    output_directory = "processed_images"
    new_size = (800, 600)

    process_images_parallel(input_images, output_directory, new_size)


if __name__ == "__main__":
    main()
