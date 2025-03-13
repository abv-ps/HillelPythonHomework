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
import asyncio
import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple

import aioconsole

from logger_config import get_logger

logger = get_logger(__name__, "validate_filtration.log")


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
        Initializes the UserInputValidator with predefined filter modes and messages.
        """
        self.filter_modes = {
            "1": "Filter by a specific date or date range",
            "2": "Filter by the last X days",
            "3": "Filter news from a specific start date",
            "4": "Filter news until a specific end date",
            "0": "No filtering"
        }

        self.prompts = {
            "select_filter_mode": "Please select a news filtering mode by date: ",
            "get_days_input": "Enter the number of days (Enter '0' for no filtering, "
                              "positive integer number",
            "get_date_input": "Enter the start date (Enter '0' for no filtering, "
                              "format YYYY-MM-DD): ",
            "get_date_range_input": "Enter a specific date or a date range "
                                    "(Enter '0' for no filtering, "
                                    "format: YYYY-MM-DD, Optional[YYYY-MM-DD]):",
            "get_date_before_input": "Enter the end date (Enter '0' for no filtering, "
                                     "format YYYY-MM-DD): "
        }

    def check_no_filter(self, user_input: str | None) -> bool:
        """
        Checks if the user input is "0" (no filtering mode) and prints a message if true.

        Args:
            user_input (str|None): The user input string.

        Returns:
            bool: True if the input is "0", otherwise False.
        """
        if user_input == "0" or user_input is None:
            return True
        return False

    async def get_user_input(self, prompt_key: str) -> Optional[str]:
        """
        Accepts user input and validates it against given options.

        Args:
            prompt_key (str): The key of the input prompt in the prompts dictionary.

        Returns:
            Optional[str]: The selected valid choice or None if "0" is selected.

        Raises:
            KeyboardInterrupt: If the user interrupts the process.
        """
        try:
            prompt = self.prompts.get(prompt_key, "")
            if prompt_key == "select_filter_mode":
                filter_modes_str = '\n'.join([f"{key}: {value}"
                                              for key, value in self.filter_modes.items()])
                prompt = f"{prompt}\n{filter_modes_str}"
            while True:
                user_input = (await aioconsole.ainput(
                    (f"{prompt}\nYour choice: "))).strip()
                if self.check_no_filter(user_input):
                    logger.warning("\nNo filtering mode selected. Exiting filter selection."
                                   "\nStarting to scrape the news...")
                    logger.handlers[0].flush()
                    return None
                return user_input
        except KeyboardInterrupt:
            logger.error("\nProcess interrupted by user. Exiting...")
            sys.exit(0)
        except asyncio.CancelledError:
            logger.error("\nInput operation was cancelled.")
            sys.exit(0)

    async def get_days_input(self, prompt_key: str) -> Optional[str]:
        """
        Gets the number of days for filtering news articles by a date range.

        Args:
            prompt_key (str): The key for the prompt message.

        Returns:
            Optional[str]: The calculated start date in 'YYYY-MM-DD' format, or None if "0" is selected.
        """
        while True:
            days_input = await self.get_user_input(prompt_key)
            if self.check_no_filter(days_input):
                return None

            try:
                days: int = int(days_input) - 1
                if days < 0:
                    raise ValueError("Number of days cannot be negative.")
                result = str(((datetime.now() - timedelta(days=days))).strftime("%Y-%m-%d"))
                logger.info("\nUser selected days range: %s days, "
                            "calculated start date: %s", days + 1, result)
                logger.warning("\n[FILTER] Starting to filter news articles for "
                               "%s days from %s...", days + 1, result)
                return result
            except ValueError:
                logger.error("\nError: %s is not a valid number. ", days_input)

    async def get_date_input(self, prompt_key: str) -> Optional[str]:
        """
        Gets a single date input from the user.

        Args:
            prompt_key (str): The key for the prompt message.

        Returns:
            Optional[str]: The date string in 'YYYY-MM-DD' format, or None if "0" is selected.
        """
        while True:
            try:
                date_input = await self.get_user_input(prompt_key)
                if self.check_no_filter(date_input):
                    return None
                datetime.strptime(date_input, "%Y-%m-%d")
                logger.info("User entered valid date: %s", date_input)
                logger.warning("\n[FILTER] Starting to filter news articles from %s...  ",
                               date_input)
                return date_input
            except ValueError:
                logger.error("\nInvalid date format entered: %s", date_input)

    async def get_date_range_input(self, prompt_key: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Gets a date range input from the user.

        Args:
            prompt_key (str): The key for the prompt message.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing start and end dates,
                                                 or None if "0" is selected.
        """
        while True:
            range_input = await self.get_user_input(prompt_key)
            if self.check_no_filter(range_input):
                return None, None
            try:
                dates = [date.strip() for date in range_input.split(",")]
                if not (0 < len(dates) <= 2):
                    raise ValueError("Invalid number of dates provided.")
                start_date = dates[0]
                end_date = str((datetime.strptime(dates[-1], "%Y-%m-%d") + timedelta(days=1)
                                ).strftime("%Y-%m-%d"))
                logger.info("User selected date range: %s - %s", start_date, end_date)
                logger.warning("\n[FILTER] Starting to filter news articles from %s "
                               "to %s...", start_date,
                               datetime.strptime(dates[-1], "%Y-%m-%d"))
                return start_date, end_date
            except ValueError:
                logger.error("Invalid format entered: %s ", range_input)

    async def get_date_before_input(self, prompt_key: str) -> Optional[str]:
        """
        Gets a date input for filtering news articles before a specific date.

        Args:
            prompt_key (str): The key for the prompt message.

        Returns:
            Optional[str]: The date string in 'YYYY-MM-DD' format, or None if no input is given.
        """
        while True:
            date_input = await self.get_user_input(prompt_key)
            if self.check_no_filter(date_input):
                return None
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                logger.info("\nUser entered valid end date: %s", date_input)
                logger.warning("\n[FILTER] Starting to filter news articles before %s",
                               date_input)
                return date_input
            except ValueError:
                logger.error("\nInvalid end date format entered: %s", date_input)

    async def select_filter_mode(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Prompts the user to select a filtering mode and retrieves
        the necessary date values for filtering.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing
                                                 the start and end dates for filtering.
                Either value may be None if no filter is applied.
        """
        filter_mode = await self.get_user_input("select_filter_mode")
        if filter_mode is None:
            return None, None
        valid_options = set(self.filter_modes.keys())
        if filter_mode is None or filter_mode not in valid_options:
            logger.warning("\nInvalid choice: %s. Valid options: %s",
                           filter_mode, list(valid_options))
            return await self.select_filter_mode()

        logger.info("User selected filter mode: %s", filter_mode)

        if filter_mode == "1":
            return await self.get_date_range_input("get_date_range_input")
        if filter_mode == "2":
            return await self.get_days_input("get_days_input"), None
        if filter_mode == "3":
            return await self.get_date_input("get_date_input"), None
        if filter_mode == "4":
            return None, await self.get_date_before_input("get_date_before_input")
        return None, None
