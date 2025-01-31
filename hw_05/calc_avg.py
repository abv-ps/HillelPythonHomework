import os


class EmptyFileError(Exception):
    """
    Exception raised when the file is empty and average calculation is not possible.
    """

    def __init__(self, message="Error: The file is empty. Average calculation is not possible."):
        super().__init__(message)


class SingleLineFileError(Exception):
    """
    Exception raised when the file contains only one line, making the average equal to that value.
    """

    def __init__(self, value):
        message = f"Error: The file contains only one line. The average is equal to the only value: {value}."
        super().__init__(message)
        self.value = value


def get_file_for_avg() -> str:
    """
    Prompts the user to select an input text file.

    Returns:
        str: The selected file path.
    """
    default_path = os.getcwd()
    input_dir = input(f"Enter folder path with files to calculate (default: {default_path}): ").strip() or default_path

    while not os.path.isdir(input_dir):
        print("Error: Invalid directory path.")
        input_dir = input("Enter a valid folder path: ").strip()

    available_files = [f for f in os.listdir(input_dir) if
                       os.path.isfile(os.path.join(input_dir, f)) and f.endswith(".txt")]

    if not available_files:
        print("Error: No text files found in the selected directory.")
        exit()

    print("Available text files:")
    for i, file in enumerate(available_files, start=1):
        print(f"{i}: {file}")

    while True:
        try:
            file_index = int(input("Enter the number of the file you want to calculate: ")) - 1
            if 0 <= file_index < len(available_files):
                break
            else:
                print("Error: Invalid selection. Try again.")
        except ValueError:
            print("Error: Please enter a valid number.")

    input_file_path = os.path.join(input_dir, available_files[file_index])
    return input_file_path


def calculate_average(file_path: str) -> float:
    """
    Reads a text file containing numbers and calculates their average.

    Raises:
        EmptyFileError: If the file is empty.
        SingleLineFileError: If the file contains only one number.

    Returns:
        float: The calculated average.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            numbers = file.readlines()

        if not numbers:
            raise EmptyFileError()

        numbers = [float(num.strip()) for num in numbers]

        if len(numbers) == 1:
            raise SingleLineFileError(numbers[0])

        return sum(numbers) / len(numbers)

    except FileNotFoundError:
        print("Error: File not found!")
        exit()
    except ValueError:
        print("Error: File contains non-numeric data!")
        exit()


if __name__ == "__main__":
    try:
        file_path = get_file_for_avg()
        avg = calculate_average(file_path)
        print(f"Average: {avg}")
    except EmptyFileError as e:
        print(e)
    except SingleLineFileError as e:
        print(e)
