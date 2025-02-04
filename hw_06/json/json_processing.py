import json
from typing import List, Tuple, TypedDict
from get_file_from_directory import get_file_from_directory


# Define a structure for books
class Book(TypedDict):
    назва: str
    автор: str
    рік: int
    наявність: bool


# Function to load books from a JSON file
def load_books(fn: str) -> Tuple[List[Book], str]:
    """Tries to load books from a JSON file, allowing the user to select a different file if not found."""
    max_attempts = 3
    attempt_count = 0

    while attempt_count < max_attempts:
        try:
            with open(fn, "r", encoding="utf-8") as f:
                books: List[Book] = json.load(f)
            return books, fn  # Return books and the final file name used
        except FileNotFoundError:
            print(f"File '{fn}' not found. Attempting to select a new file...")
            attempt_count += 1
            fn = get_file_from_directory()
        except json.JSONDecodeError:
            print(f"Error decoding JSON from '{fn}'.")
            return [], fn  # Return an empty list but keep the last valid filename

    return [], fn  # Return an empty list if all attempts fail


# Function to display available books
def available_books(books: List[Book]) -> None:
    """Displays books that are in stock."""
    print("Books іn stock:")
    for book in books:
        if book["наявність"]:
            print(f"Book {book['назва']}, year of publication {book['рік']} by {book['автор']} is in stock.")


# Function to add a new book to a JSON file
def add_book(fn: str, new_book: dict) -> None:
    """Adds a new book to the JSON file without reading the entire file into memory."""
    try:
        with open(fn, "r+", encoding="utf-8") as f:
            # Moved to the end of the file
            f.seek(0, 2)

            # Check if the file is not empty, except for the closing of the ']' array
            if f.tell() > 2:
                # Now move to the end and look for the penultimate character
                f.seek(f.tell() - 1)
                char = f.read(1)
                # Skip extra spaces, newlines, and tabs
                while char in ['\n', ' ', '\t'] and f.tell() > 1:
                    f.seek(f.tell() - 3)
                    char = f.read(1)
                # If there is a closing bracket ']', add a comma
                if char == "]":
                    f.seek(f.tell() - 3)  # Return to '}'
                    f.write(",\n")  # Add a comma before the new element
            json_data = json.dumps(new_book, ensure_ascii=False, separators=(',', ': '))
            f.write(f"    {json_data}\n]")

        print(f"New book '{new_book['назва']}', year of publication {new_book['рік']} "
              f"by {new_book['автор']} has been added.")
    except Exception as e:
        print(f"Error adding book: {e}")


def get_valid_year() -> int:
    """Ensures the user enters a valid integer year."""
    while True:
        try:
            year = int(input("Enter the year of publication of the new book: "))
            if year < 0:
                raise ValueError
            return year
        except ValueError:
            print("Error: Please enter a valid positive integer for the year.")


def get_valid_availability() -> bool:
    """Ensures the user enters a valid availability status."""
    while True:
        user_input = input("Is the book in stock? (true/false, yes/no, 1/0): ").strip().lower()
        if user_input in ["true", "yes", "1"]:
            return True
        elif user_input in ["false", "no", "0"]:
            return False
        else:
            print("Error: Please enter 'true', 'false', 'yes', 'no', '1' or '0'.")


def main() -> None:
    fn = "books.json"

    books, fn = load_books(fn)

    available_books(books)

    # Get new book details
    new_book: Book = {
        "назва": input("Enter the name of the new book to add: ").strip(),
        "автор": input("Enter the author of the new book: ").strip(),
        "рік": get_valid_year(),
        "наявність": get_valid_availability(),
    }

    add_book(fn, new_book)


if __name__ == "__main__":
    main()
