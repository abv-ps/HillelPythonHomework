"""
This module provides functionality for managing user interactions with a paginated list of items.
It includes loading data from a CSV file, navigating through pages of items, handling cases when no items are found,
and updating attempts for user input.

Key Components:
- `load_csv`: Loads data from a CSV file and returns it as a list of lists.
- `choose_page_action`: Prompts the user to choose an item from a paginated list or navigate between pages.
- `handle_no_items_found`: Handles cases where no items are found and allows the user to choose an action.
- `update_attempts`: Increments the attempt count and checks if the maximum attempts have been reached.

Usage:
- Use `load_csv` to read CSV data into a list of lists.
- Use `choose_page_action` to manage navigation and selection within paginated lists of items.
- Use `handle_no_items_found` to provide an interface for retrying searches or showing all items.
- Use `update_attempts` to track and limit the number of user input attempts.
"""

import csv
from typing import Callable, Any, Optional


def load_csv(filename: str) -> list[list[str]]:
    """
    Loads a CSV file and returns its content as a list of lists.

    Args:
        filename (str): The name of the CSV file.

    Returns:
        list[list[str]]: List of rows from the CSV file, excluding the header.
        Each inner list contains string representations of values.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data[1:]


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

        if selection == 'on' and action.isdigit():
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


def handle_no_items_found(item_name: str, items_func: Callable[[], Any],
                          retry_func: Callable[[], None]) -> Optional[str]:
    """
    Handles the case when no items are found and asks the user what to do next.

    Args:
        item_name (str): The name of the item (e.g., "movie", "actor").
        items_func (Callable[[], Any]): Function that returns all items (e.g., show_all_movies).
        retry_func (Callable[[], None]): Function to retry the search action.

    Returns:
        Optional[str]: Returns the result of the action taken by the user (e.g., result of retry_func, items_func,
                       or the action of returning to the main menu). If returning to the main menu, it calls
                       `go_to_main_menu()`.

    Description:
        This function prompts the user with three options when no items matching their search criteria are found:
        1. Retry the search for the specified item.
        2. Display all available items of the specified type.
        3. Exit to the main menu.

        Based on the user's input, the function will either retry the search, display all items, or return to the main menu.
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
            return retry_func()
        elif retry_choice == '2':
            print(f"Showing all {item_name}s...")
            return items_func()
        elif retry_choice == '3' or retry_choice in ['exit', 'q']:
            from hw_10.movie_db.ui.movie_database import go_to_main_menu
            return go_to_main_menu("According to your choice 'exit'")
        else:
            print("Invalid option. Please select 1, 2, or 3.")


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

def get_input() -> str:
    """
    Prompts the user for input from the console.

    This function uses the built-in `input()` function to get a line of text
    entered by the user. It returns the input as a string.

    Returns:
        str: The user's input as a string.
    """
    return input()



