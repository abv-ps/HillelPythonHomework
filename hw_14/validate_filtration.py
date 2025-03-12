"""
Module for handling user input validation related to date-based news filtering.

This module contains the `UserInputValidator` class, which provides various methods
to prompt the user for different types of date-based filters for news articles.

The filters allow the user to specify a particular date, a date range, or relative date ranges
(e.g., last X days). It also provides the option for filtering by news articles
before or after specific dates.

Class:
    UserInputValidator:
        A class that provides methods for selecting and validating date filters:
        - Filter by a specific date or date range.
        - Filter by the last X days.
        - Filter news from a specific start date.
        - Filter news until a specific end date.
        - No filtering option.

Methods:
    - get_user_input: Accepts user input and validates it against a list of valid options.
    - get_days_input: Prompts the user for the number of days and calculates a start date
      based on that input.
    - get_date_input: Prompts the user for a single date input and validates its format.
    - get_date_range_input: Prompts the user for a date range input and validates the format.
    - get_date_before_input: Prompts the user for a date input to filter news articles
      before that date.
    - select_filter_mode: Displays a menu of filter options and returns the selected filter,
      along with the corresponding dates for filtering.

Usage:
    1. Instantiate the `UserInputValidator` class.
    2. Use `select_filter_mode()` to prompt the user to select a filtering mode.
    3. Depending on the selected mode, the corresponding methods will be called
       to gather the necessary date inputs.
    4. The method will return the relevant start and end dates
       (if applicable) for filtering the news articles.
"""


import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple


class UserInputValidator:
    """
    A class that handles user input validation for date-based news filtering.
    It provides methods for selecting and validating different types of filters:
    - Specific date or date range.
    - Filtering by the last X days.
    - Filtering by a start date or end date.

    Methods:
        - get_user_input: Accepts and validates user input against a list of valid options.
        - get_days_input: Gets the number of days for filtering by a specific date range.
        - get_date_input: Accepts and validates a single date input.
        - get_date_range_input: Accepts and validates a date range input.
        - get_date_before_input: Accepts and validates a date input
          for filtering before a specific date.
        - select_filter_mode: Prompts the user to select a filtering mode
          and returns the appropriate dates for filtering.
    """

    def __init__(self) -> None:
        """
        Initializes the UserInputValidator with predefined filter modes.
        """
        self.filter_modes = {
            "1": "Filter by a specific date or date range",
            "2": "Filter by the last X days",
            "3": "Filter news from a specific start date",
            "4": "Filter news until a specific end date",
            "0": "No filtering"
        }

    def get_user_input(self, prompt: str, valid_options: set) -> str:
        """
        Accepts user input and validates it against given options.

        Args:
            prompt (str): The input prompt message.
            valid_options (set): A set of valid choices.

        Returns:
            str: The selected valid choice.

        Raises:
            KeyboardInterrupt: If the user interrupts the process.
        """
        try:
            while True:
                user_input = input(f"{prompt}\nYour choice: ").strip()
                if user_input in valid_options:
                    return user_input
                print(f"Invalid choice. Please select one of the available options: "
                      f"{list(valid_options)}")
        except KeyboardInterrupt:
            print("\nProcess interrupted. Exiting...")
            sys.exit(0)

    def get_days_input(self, prompt: str, default: str) -> Optional[str]:
        """
        Gets the number of days for filtering news articles by a date range.

        Args:
            prompt (str): The input prompt message.
            default (str): The default value if no input is given.

        Returns:
            Optional[str]: The calculated start date in 'YYYY-MM-DD' format, or None if no filter.
        """
        try:
            days_input = input(f"{prompt} (default: {default}): ").strip() or default
            days = int(days_input)
            if days < 0:
                raise ValueError("Number of days cannot be negative.")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            return start_date
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
            return self.get_days_input(prompt, default)

    def get_date_input(self, prompt: str) -> Optional[str]:
        """
        Gets a single date input from the user.

        Args:
            prompt (str): The input prompt message.

        Returns:
            Optional[str]: The date string in 'YYYY-MM-DD' format, or None if no input is given.
        """
        try:
            date_input = input(f"{prompt} (format YYYY-MM-DD): ").strip()
            if not date_input:
                return None
            datetime.strptime(date_input, "%Y-%m-%d")  # Validate format
            return date_input
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
            return self.get_date_input(prompt)

    def get_date_range_input(self, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Gets a date range input from the user.

        Args:
            prompt (str): The input prompt message.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing start and end dates,
                                                 or None if no range is given.
        """
        try:
            range_input = input(f"{prompt} (format: YYYY-MM-DD, Optional[YYYY-MM-DD]): ").strip()
            if not range_input:
                return None, None

            dates = range_input.split(",")
            if len(dates) == 1:
                specific_date = datetime.strptime(dates[0].strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
                return specific_date, specific_date
            if len(dates) == 2:
                start_date = datetime.strptime(dates[0].strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
                end_date = datetime.strptime(dates[1].strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
                return start_date, end_date
            raise ValueError
        except ValueError:
            print("Invalid format. Please enter a date or a date range "
                  "in the format YYYY-MM-DD, YYYY-MM-DD.")
            return self.get_date_range_input(prompt)

    def get_date_before_input(self, prompt: str) -> Optional[str]:
        """
        Gets a date input for filtering news articles before a specific date.

        Args:
            prompt (str): The input prompt message.

        Returns:
            Optional[str]: The date string in 'YYYY-MM-DD' format, or None if no input is given.
        """
        try:
            date_input = input(f"{prompt} (format YYYY-MM-DD): ").strip()
            if not date_input:
                return None
            datetime.strptime(date_input, "%Y-%m-%d")  # Validate format
            return date_input
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
            return self.get_date_before_input(prompt)

    def select_filter_mode(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Prompts the user to select a filtering mode and retrieves
        the necessary date values for filtering.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing
                                                 the start and end dates for filtering.
                Either value may be None if no filter is applied.
        """
        filter_modes_str = '\n'.join([f"{key}: {value}" for key, value
                                      in self.filter_modes.items()])

        filter_mode = self.get_user_input(
            f"Please select a news filtering mode by date: \n{filter_modes_str}",
            set(self.filter_modes.keys())
        )

        if filter_mode == "1":
            return self.get_date_range_input("Enter a specific date or a date range")
        if filter_mode == "2":
            start_date = self.get_days_input("Enter the number of days", "7")
            return start_date, None
        if filter_mode == "3":
            start_date = self.get_date_input("Enter the start date")
            return start_date, None
        if filter_mode == "4":
            end_date = self.get_date_before_input("Enter the end date for filtering news")
            return None, end_date
        return None, None
