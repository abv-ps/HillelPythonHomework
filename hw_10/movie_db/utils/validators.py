"""
This module provides functionality for managing database operations and validating user input.

`Validator` Class:
   - A class for validating user input such as movie titles, actor names, and genres
     using regular expressions.
   - Includes methods like:
     - `validate`: A generic method to validate input based on predefined patterns.
     - `validate_title_movie`: A method for validating movie titles with retry logic.
     - `validate_actor_name_genre`: A method for validating actor names or genres with retry logic.
     - `validate_year`: A method for validating birth or release year with retry logic.

Usage:
- The `Validator` class can be instantiated for validating movie titles, actor names,
  and genres using regex-based validation.
- The `case_insensitive_collation` function can be used in SQLite queries to compare strings
  without regard to case.

This module is intended to streamline database operations with cursor availability checks
and simplify the validation of user input in a variety of use cases.
"""

import re
import time
from typing import Tuple

from ..utils.helpers import update_attempts


class Validator:
    """
    A class for validating movie titles, actor names, and genres using regular expressions.

    This class provides methods to validate various input types such as movie titles, actor names, and genres.
    The validation is based on predefined regular expressions. The class also allows multiple validation attempts
    with a limit on the number of retries.

    Attributes:
        patterns (dict): A dictionary containing regex patterns for validating different types of inputs.
                          Each key corresponds to a specific validation type (e.g., 'title_movie', 'actor_name_genre').
        year_ranges (dict): A dictionary specifying valid year ranges for 'birth' and 'release' years.
                            Keys are 'birth' and 'release', with values as tuples (min_year, max_year).

    Methods:
        validate(text: str, item_name: str, validation_type: str) -> bool:
            Validates a given text input based on the specified validation type.

        validate_title_movie(text: str, item_name: str, max_attempts: int = 3) -> Tuple[bool, str]:
            Validates a movie title with a limited number of attempts.

        validate_actor_name_genre(text: str, item_name: str, max_attempts: int = 3) -> Tuple[bool, str]:
            Validates an actor name or genre with a limited number of attempts.

        validate_year(year: int, year_type: str, max_attempts: int = 3) -> Tuple[bool, int]:
            Validates a year (either birth year or release year) within the specified range with retry logic.
    """

    EXIT_COMMANDS = {"exit", "q"}

    def __init__(self) -> None:
        """
        Initializes the Validator with predefined regex patterns for movie titles, actor names, and genres.

        The patterns are as follows:
        - "title_movie": Validates movie titles, which should contain at least two letters and may include
                          spaces, hyphens, and other special characters.
        - "actor_name_genre": Validates actor names or genres, which should contain at least two letters and
                               may include spaces, underscores, and hyphens.

        Initializes the following attribute:
            patterns (dict): A dictionary containing regex patterns for different input types.
            year_ranges (dict): A dictionary containing valid year ranges for 'birth' and 'release'.
        """
        self.patterns = {
            "title_movie": r"^([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ0-9-_@]{2,})(?:\s([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ0-9-_@]{2,}))*$",
            "actor_name_genre": r"^([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ_-]{2,})(?:\s([A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ_-]{2,}))*$"
        }
        current_year = time.localtime().tm_year
        self.year_ranges = {
            "birth": (1880, current_year),
            "release": (1895, current_year)
        }

    def validate(self, text: str, item_name: str, validation_type: str) -> bool:
        """
        Validates a given text input based on the specified validation type.

        Args:
            text (str): The input text to be validated (e.g., a movie title, actor name, or genre).
            item_name (str): The name of the item being validated (e.g., 'title', 'actor name').
            validation_type (str): The type of validation ('title_movie', 'actor_name_genre').

        Returns:
            bool: True if the text is valid according to the pattern, False otherwise.

        If the `validation_type` is invalid, a message will be printed to indicate the issue.
        """
        pattern = self.patterns.get(validation_type)
        if not pattern:
            print(f"Invalid validation type: {validation_type}")
            return False

        if re.match(pattern, text):
            return True
        print(f"Invalid {item_name}! The {item_name} should consist of at least two letters at the beginning "
              "with a possible separator and at least two letters after it.")
        return False

    def validate_title_movie(self, text: str, item_name: str, max_attempts: int = 3) -> Tuple[bool, str]:
        """
        Validates a movie title with a limited number of attempts.

        Args:
            text (str): The movie title to be validated.
            item_name (str): The name of the item being validated (e.g., 'movie title').
            max_attempts (int): The maximum number of attempts allowed (default is 3).

        Returns:
            Tuple[bool, str]: A tuple where the first element is True if the title is valid, False otherwise,
                               and the second element is the validated or last entered text.

        The user is prompted to re-enter the title if it is invalid, up to the maximum number of attempts.
        If the user enters "exit" or "q", the validation stops.
        """
        attempts = 0
        while attempts < max_attempts and text not in self.EXIT_COMMANDS:
            if self.validate(text, item_name, "title_movie"):
                return True, text
            attempts = update_attempts(attempts, max_attempts)
            if attempts >= max_attempts:
                return False, text
            text = input(f"Please enter the {item_name} again: ").strip()
        return False, text

    def validate_actor_name_genre(self, text: str, item_name: str, max_attempts: int = 3) -> Tuple[bool, str]:
        """
        Validates an actor name or genre with a limited number of attempts.

        Args:
            text (str): The actor name or genre to be validated.
            item_name (str): The name of the item being validated (e.g., 'actor name' or 'genre').
            max_attempts (int): The maximum number of attempts allowed (default is 3).

        Returns:
            Tuple[bool, str]: A tuple where the first element is True if valid, False otherwise,
                               and the second element is the validated or last entered text.

        The user is prompted to re-enter the name or genre if it is invalid, up to the maximum number of attempts.
        If the user enters "exit" or "q", the validation stops.
        If the maximum attempts are reached, an error message is shown.
        """
        attempts = 0
        while attempts < max_attempts and text not in self.EXIT_COMMANDS:
            if self.validate(text, item_name, "actor_name_genre"):
                return True, text

            attempts = update_attempts(attempts, max_attempts)

            if attempts >= max_attempts:
                break

            text = input(f"Please enter the {item_name} again: ")

        if text not in self.EXIT_COMMANDS:
            print("Maximum attempts reached. Invalid input.")

        return False, text

    def validate_year(self, year: int, year_type: str, max_attempts: int = 3) -> Tuple[bool, int]:
        """
        Validates a year (either birth year or release year) within the specified range, with a limited number of attempts.

        Args:
            year (int): The year to be validated.
            year_type (str): The type of the year ('birth' or 'release').
            max_attempts (int): The maximum number of attempts allowed (default is 3).

        Returns:
            Tuple[bool, int]: A tuple where the first element is True if the year is valid, False otherwise,
                               and the second element is the validated or last entered year.

        If the year is invalid, the user is prompted to re-enter it, up to the maximum number of attempts.
        If the user enters "exit" or "q", the validation stops.
        """
        if year_type not in self.year_ranges:
            raise ValueError(f"Invalid year type: {year_type}. Must be 'birth' or 'release'.")

        min_year, max_year = self.year_ranges[year_type]
        attempts = 0

        while attempts < max_attempts:
            if min_year <= year <= max_year:
                return True, year

            attempts += 1
            if attempts >= max_attempts:
                return False, year

            year_input = input(f"Enter a valid {year_type} year ({min_year}-{max_year}): ").strip()
            if year_input.lower() in self.EXIT_COMMANDS:
                return False, year

            try:
                year = int(year_input)
            except ValueError:
                continue

        return False, year
