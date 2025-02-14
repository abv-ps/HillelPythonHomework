"""
This module provides a function to convert a date string from the format DD/MM/YYYY
to YYYY-MM-DD. It handles valid date strings in the expected format and returns
the reformatted date or None if the input does not match the expected format.
"""

import re
from typing import Optional


def convert_date_format(date: str) -> Optional[str]:
    """
    Converts a date from the format DD/MM/YYYY to YYYY-MM-DD.

    This function takes a date string in the format "DD/MM/YYYY" and converts it to
    the format "YYYY-MM-DD". If the input date does not match the expected format,
    it returns None.

    Args:
        date (str): The date string in the format DD/MM/YYYY.

    Returns:
        Optional[str]: The date string in the format YYYY-MM-DD,
                       or None if the input date does not match the expected format.

    Example:
        >>> convert_date_format("14/02/2025")
        '2025-02-14'

        >>> convert_date_format("31/04/2025")
        '2025-04-31'

        >>> convert_date_format("2025-02-14")
        None
    """
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", date):
        return None

    return re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", date)


# Example usage:
date = "14/02/2025"
formatted_date = convert_date_format(date)
if formatted_date:
    print(f"Converted date: {formatted_date}")
else:
    print("Invalid date format.")
