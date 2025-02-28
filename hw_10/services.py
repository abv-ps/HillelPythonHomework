"""
- `choose_page_action`: Handles pagination and item selection.
"""
import re
from typing import Callable, Any, Tuple


def ensure_cursor(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that ensures the database cursor is available before executing the function.

    This decorator checks if the 'cursor' attribute exists and is not None. If the cursor
    is unavailable, a ValueError will be raised. If the cursor is available, the decorated
    function is executed.

    Args:
        func (Callable[..., Any]): The function to be decorated. It is expected to take `self`
                                   as its first argument and any additional arguments.

    Returns:
        Callable[..., Any]: The wrapped function that checks for the cursor availability before
                            execution.

    Raises:
        ValueError: If the database cursor is not available.
    """

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'cursor') or self.cursor is None:
            raise ValueError("Database connection not established.")
        return func(self, *args, **kwargs)

    return wrapper


class AutoEnsureCursorMeta(type):
    """
    A metaclass that automatically applies the `ensure_cursor` decorator to all methods of a class,
    except for methods that do not require it (like `__init__`, `__enter__`, `__exit__`).
    """
    skip_cursor_check_methods = {'__init__', '__enter__', '__exit__'}

    def __new__(mcs, name, bases, dct):
        # Apply ensure_cursor to all methods except special ones
        for key, value in dct.items():
            if callable(value) and key not in mcs.skip_cursor_check_methods:
                dct[key] = ensure_cursor(value)  # Apply the decorator to the method
        return super().__new__(mcs, name, bases, dct)


class Validator:
    def __init__(self):
        self.patterns = {
            "title_movie": r"^([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ0-9-_@]{2,})(?:\s([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ0-9-_@]{2,}))*$",
            "actor_name_genre": r"^([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ_-]{2,})(?:\s([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ_-]{2,}))*$"
        }

    def validate(self, text: str, item_name: str, validation_type: str) -> bool:
        pattern = self.patterns.get(validation_type)
        if not pattern:
            print(f"Invalid validation type: {validation_type}")
            return False

        if re.match(pattern, text):
                return True
        print(f"Invalid {item_name}! The {item_name} should consist of at least two letters "
                  "at the beginning with a possible separator and at least two letters after it.")
        return False

    def validate_title_movie(self, text: str, item_name: str, max_attempts: int = 3) -> Tuple[bool, str]:
        """Validate movie title with a limited number of attempts."""
        attempts = 0
        while attempts < max_attempts and text not in {"exit", "q"}:
            if self.validate(text, item_name, "title_movie"):
                return True, text
            attempts = update_attempts(attempts, max_attempts)
            if attempts >= max_attempts:
                return False, text
            text = input(f"Please enter the {item_name} again: ").strip()
        return False, text

    def validate_actor_name_genre(self, text: str, item_name: str, max_attempts: int = 3) -> Tuple[bool, str]:
        """Validate actor name or genre with a limited number of attempts using update_attempts."""
        attempts = 0
        while attempts < max_attempts and text not in {"exit", "q"}:
            if self.validate(text, item_name, "actor_name_genre"):
                return True, text

            attempts = update_attempts(attempts, max_attempts)

            if attempts >= max_attempts:
                break

            text = input(f"Please enter the {item_name} again: ")

        if text not in {"exit", "q"}:
            print("Maximum attempts reached. Invalid input.")

        return False, text


def choose_page_action(items: list, item_name: str, current_page: int = 1,
                       selection: str = 'off', results_per_page: int = 15,
                       max_attempts: int = 3) -> str:
    """
    Prompts the user to choose an item or navigate between pages (next, prev).

    Args:
        items (list): The list of items to select from (e.g., movies, actors).
        item_name (str): The name of the item (e.g., "movie", "actor").
        current_page (int): The current page number.
        selection (str): Determines if the user is prompted to select an item ('on')
                         or just navigate between pages. Default is 'off'.
        results_per_page (int): The number of items to display per page (default is 15).
        max_attempts (int): The maximum number of attempts for user input.

    Returns:
        str: The name of the selected item or 'exit' to return to the main menu.
    """
    total_pages = (len(items) + results_per_page - 1) // results_per_page
    attempts = 0

    while attempts < max_attempts:
        start_index = (current_page - 1) * results_per_page
        end_index = start_index + results_per_page
        page_items = items[start_index:end_index]

        print(f"Page {current_page} of {total_pages}\n")
        print(f"Showing {item_name}s {start_index + 1}-{start_index + len(page_items)} of {len(items)}\n")
        print(f"Type 'next'|'+1' to go to the next page or 'prev'|'-1' to go to the previous page:")

        if selection == 'on':
            print(f"Select a {item_name} ({start_index + 1}-{start_index + len(page_items)})")

        for i, item in enumerate(page_items, 1):
            print(f"{start_index + i}. {item}")

        print("Type 'exit'/'q' to return to the main menu")

        action = input("Your choice: ").strip().lower()

        if action in {"exit", "q"}:
            return "exit"

        if action.isdigit():
            choice_index = int(action) - 1
            if 0 <= choice_index < len(page_items):
                print(page_items[choice_index])
                return page_items[choice_index]
            print("Invalid selection. Please try again.")
        elif action in ['next', '+1']:
            if current_page < total_pages:
                current_page += 1
                continue
            print("You are already on the last page.")
        elif action in ['prev', '-1']:
            if current_page > 1:
                current_page -= 1
                continue
            print("You are already on the first page.")

        print("\nInvalid input. Please try again.")
        attempts = update_attempts(attempts, max_attempts)
        if attempts >= max_attempts:
            return "exit"

    return "exit"


def update_attempts(attempts: int, max_attempts: int) -> int:
    """
    Increments the number of attempts and checks if the limit is reached.

    Args:
        attempts (int): The current attempt count.
        max_attempts (int): The maximum allowed attempts.

    Returns:
        int: Updated attempt count.
    """
    attempts += 1
    if attempts >= max_attempts:
        print("Maximum attempts reached.")
        return max_attempts
    print(f"You have {max_attempts - attempts} attempts left.")
    return attempts


def go_to_main_menu() -> None:
    """
    Prompts the user to return to the main menu.

    Args:
        immediate_exit (bool): If True, immediately returns to the main menu.
    """
    print("Returning to the main menu...")
    return None


def case_insensitive_collation(str1, str2):
    """
    A simple case-insensitive comparison function for SQLite.
    """
    return (str1.lower() > str2.lower()) - (str1.lower() < str2.lower())


def handle_no_items_found(item_name: str, items_func: Callable[[], Any],
                          retry_func: Callable[[], None]) -> None:
    """
    Handles the case when no items are found and asks the user what to do next.

    Args:
        item_name (str): The name of the item (e.g., "movie", "actor").
        items_func (Callable[[], Any]): Function that returns all items (e.g., show_all_movies).
        retry_func (Callable[[], None]): Function to retry the search action.

    Returns:
        None
    """
    print(f"No {item_name} found with that search.")

    while True:
        retry_choice = input(
            f"\nWhat would you like to do next? Choose an option:\n"
            f"1. Search again for a {item_name}\n"
            f"2. Show all {item_name}s\n"
            f"3. Exit to the main menu\n"
            f"Please enter the option number (1-3): ").strip()

        if retry_choice == '1':
            print(f"Let's try searching again for the {item_name}...")
            retry_func()
            return
        elif retry_choice == '2':
            print(f"Showing all {item_name}s...")
            return items_func()
        elif retry_choice == '3' or retry_choice in ['exit', 'q']:
            print("Returning to the main menu...")
            return go_to_main_menu()
        else:
            print("Invalid option. Please select 1, 2, or 3.")
