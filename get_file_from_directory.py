import os

def get_file_from_directory() -> str:
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

    processing_files = [f for f in os.listdir(processing_path)]

    if not processing_files:
        print("Error: No files found in the selected directory.")
        exit()

    print("Available files to process:")
    for i, file in enumerate(processing_files, start=1):
        print(f"{i}: {file}")

    try:
        file_index = int(input("Enter the number of the file you want to process: ")) - 1
        if file_index < 0 or file_index >= len(processing_files):
            raise ValueError
    except ValueError:
        print("Error: Invalid selection.")
        exit()

    return os.path.join(processing_path, processing_files[file_index])