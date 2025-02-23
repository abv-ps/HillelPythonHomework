import re

import re


class Validator:
    def __init__(self):
        self.patterns = {
            "title_movie": r"^([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ0-9-_@]{2,})(?:\s([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ0-9-_@]{2,}))*$",
            "actor_name_genre": r"^([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ-_]{2,})(?:\s([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ-_]{2,}))*$"
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

    def validate_title_movie(self, text: str, item_name: str, max_attempts: int = 3) -> bool|None:
        """Validate movie title with a limited number of attempts."""
        attempts = 0
        while attempts < max_attempts and text not in {"exit", "q"}:
            if self.validate(text, item_name, "title_movie"):
                print('ЙЕС!!!')
                return True
            attempts += 1
            if attempts < max_attempts:
                print("\nTo return to the main menu, type 'exit' or 'q'.")
                print(f"You have {max_attempts - attempts} attempts left.")
                text = input(f"Enter the {item_name} again: ")
        if text not in {"exit", "q"}:
            print("Maximum attempts reached. Invalid input.")
        return go_to_main_menu(immediate_exit=True)

    def validate_actor_name_genre(self, text: str, item_name: str, max_attempts: int = 3) -> bool|None:
        """Validate actor name or genre with a limited number of attempts."""
        attempts = 0
        while attempts < max_attempts and text not in {"exit", "q"}:
            if self.validate(text, item_name, "actor_name_genre"):
                return True
            attempts += 1
            if attempts < max_attempts:
                print("\nTo return to the main menu, type 'exit' or 'q'.")
                print(f"You have {max_attempts - attempts} attempts left.")
                text = input(f"Enter the {item_name} again: ")
        if text not in {"exit", "q"}:
            print("Maximum attempts reached. Invalid input.")
        return go_to_main_menu(immediate_exit=True)


def choose_page_action(current_page: int, total_pages: int, items: list, item_name: str,
                       selection: str = 'on', results_per_page: int = 15) -> str | int:
    """
    Prompts the user to choose an item or navigate between pages (next, prev).

    Args:
        current_page (int): The current page number.
        total_pages (int): The total number of pages.
        items (list): The list of items to select from (e.g., movies, actors).
        item_name (str): The name of the item (e.g., "movie", "actor").
        selection (str): Determines if the user is prompted to select an item ('on')
        or just navigate between pages. Default is 'on'.
        results_per_page (int): The number of items to display per page (default is 15).

    Returns:
        str|int: The name of the selected item or the new current page number if user navigates between pages.
    """
    while True:
        start_index = (current_page - 1) * results_per_page
        end_index = start_index + results_per_page
        page_items = items[start_index:end_index]

        print(f"Page {current_page} of {total_pages}\n")
        print(f"Showing {item_name}s {start_index + 1}-{start_index + len(page_items)} of {len(items)}")

        for i, item in enumerate(page_items, 1):
            print(f"{start_index + i}. {item}")

        #print("\nTo return to the main menu, type 'exit' or 'q'.")

        if selection == 'on':
            choice = input(
                f"Select a {item_name} (1-{len(page_items)}) or type 'next'|'+1' to go to the next page, "
                f"type 'prev'|'-1' to go to the previous page: ").strip().lower()

            if choice in {"exit", "q"}:
                return "exit"

            if choice.isdigit():
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(page_items):
                    return page_items[choice_index][0]
                print("Invalid selection. Please try again.")
            elif choice in ['next', '+1']:
                if current_page < total_pages:
                    return current_page + 1
                print("You are already on the last page.")
            elif choice in ['prev', '-1']:
                if current_page > 1:
                    return current_page - 1
                print("You are already on the first page.")
        return "exit"

def go_to_main_menu(immediate_exit=False) -> None:
    """
    Prompts the user to return to the main menu.

    Args:
        immediate_exit (bool): If True, immediately returns to the main menu.
    """
    print("Returning to the main menu...")
    if immediate_exit:
        return None
    while input("To confirm, type 'exit' or 'q': ").strip().lower() not in {"exit", "q"}:
        print("Invalid input. Try again.")
    return None

def get_valid_movie_title(max_attempts: int = 3) -> str|None:
    """
    Prompts the user for a valid movie title, allowing a limited number of attempts.

    Args:
        max_attempts (int): Maximum number of validation attempts.

    Returns:
        str|None: The validated movie title or None if the user chooses to exit.
    """
    v = Validator()
    attempts = 0

    while attempts < max_attempts:
        text = input("Enter a part of the movie title to search for: ").strip()

        if text.lower() in {"exit", "q"}:
            return go_to_main_menu(immediate_exit=True)

        if v.validate(text, "movie title", "title_movie"):
            return text

        attempts += 1
        print(f"Invalid input. {max_attempts - attempts} attempts remaining.")

    print("Maximum attempts reached. Returning to main menu...")
    return go_to_main_menu(immediate_exit=True)