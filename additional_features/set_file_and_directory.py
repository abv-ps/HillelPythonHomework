import os

def set_file_and_directory() -> str:
    """
    Prompts the user to input a folder path, lists files, and allows selecting one.

    Returns:
        str: The selected file path.
    """
    default_path = os.getcwd()
    user_input = input(f"Enter the folder path to select a file for processing (default: {default_path}): ").strip()
    processing_path = user_input or default_path

    if not os.path.isdir(processing_path):
        print("Error: Invalid directory path.")
        exit()

    fn = input("Enter the name of the file you want to create: ")

    return os.path.join(processing_path, fn)