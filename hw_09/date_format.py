"""
This module provides a function to convert a date string from the format DD/MM/YYYY
to the format YYYY-MM-DD. It validates the input to ensure that the date is in the correct
format and is a valid calendar date (e.g., 31/04/2025 is invalid).

The function returns the reformatted date or None if the input does not match the expected
format or represents an invalid date.

Functions:
- convert_date_format(date: str) -> Optional[str]:
  Converts the input date string from DD/MM/YYYY format to YYYY-MM-DD format,
  returning None if the input format is incorrect or the date is invalid.
"""

import re
from typing import Optional
from datetime import datetime


def convert_date_format(date: str) -> Optional[str]:
    """
    Converts a date from the format DD/MM/YYYY to YYYY-MM-DD.

    This function takes a date string in the format "DD/MM/YYYY" and converts it to
    the format "YYYY-MM-DD". If the input date does not match the expected format,
    or is an invalid date (e.g., 31/04/2025), it returns None.

    Args:
        date (str): The date string in the format DD/MM/YYYY.

    Returns:
        Optional[str]: The date string in the format YYYY-MM-DD,
                       or None if the input date does not match the expected format
                       or is invalid.

    Example:
        >>> convert_date_format("14/02/2025")
        '2025-02-14'

        >>> convert_date_format("31/04/2025") is None
        True

        >>> convert_date_format("2025-02-17") is None
        True
    """
    match = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", date)
    if not match:
        return None

    day, month, year = match.groups()

    try:
        valid_date = datetime(int(year), int(month), int(day))
        return valid_date.strftime("%Y-%m-%d")
    except ValueError:
        return None  # Incorrect date (for example, 31/04/2025)

if __name__ == "__main__":
    ex_date = "17/02/2025"
    formatted_date = convert_date_format(ex_date)
    if formatted_date:
        print(f"Converted date: {formatted_date}")
    else:
        print("Invalid date format.")
