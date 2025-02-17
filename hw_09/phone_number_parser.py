"""
This module provides a function to find and format phone numbers
in various formats within a given text. It supports both well-known
and non-standard phone number formats and will standardize them
to a uniform (XXX) XXX-XXXX format.
"""

import re
from typing import List


def find_and_format_phone_numbers(text: str) -> List[str]:
    """
    Finds all phone numbers in the given text and formats them in the format:
    (XXX) XXX-XXXX.

    The function supports multiple formats of phone numbers:
    - (123) 456-7890
    - 123-456-7890
    - 123.456.7890
    - 1234567890

    It will clean up any non-digit characters and return the formatted phone numbers
    as a list of strings.

    Args:
        text (str): The input string containing phone numbers.

    Returns:
        List[str]: A list of formatted phone numbers found in the text.

    Example:
        >>> find_and_format_phone_numbers("Call me at (063) 567-2574, 099.721.4782.")
        ['(063) 567-2574', '(099) 721-4782']
    """
    # Regular expression to match different phone number formats
    pattern = r'\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}'

    # Find all phone numbers in the text
    phone_numbers = re.findall(pattern, text)

    f_numbers = []

    for number in phone_numbers:
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', number)

        # Ensure it has exactly 10 digits (to match (XXX) XXX-XXXX)
        if len(digits) == 10:
            f_number = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
            f_numbers.append(f_number)

    return f_numbers


if __name__ == "__main__":
    s = "Call me at (063) 567-2574, 067-453-3529, or 099.721.4782."
    formatted_numbers = find_and_format_phone_numbers(s)
    print(formatted_numbers)
