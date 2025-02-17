"""
This module provides functionality for reading user input with a timeout
and validating email addresses using regular expressions.

A valid email is considered to have the following format:

    example@domain.com

Where:
    - 'example' is a sequence of letters, digits, or periods (dots),
                but dots cannot appear at the start or end.
    - 'domain' is a sequence of letters or digits.
    - '.com', '.net', '.org', etc., represent the top-level domain (TLD),
                which must be between 2 and 6 characters long.

Functions:
    input_with_timeout(prompt: str, timeout: int) -> Optional[str]:
        Prompts the user for input with a specified timeout.

Usage:
    The user is prompted to enter a number of email addresses within a
            given time limit. If the input is invalid or times out
            , an error message is displayed.
"""

import re
import sys
from typing import Optional
from additional_features.input_timeout_utils import input_with_timeout


def main() -> None:
    """
    Main function to prompt the user for a number of lines and validate email inputs.
    """


num_lines: Optional[str] = input_with_timeout("Please enter the number "
                                              "of lines to test email: ", 20)

if num_lines is None or not num_lines.isdigit():
    print("Invalid input. Exiting...")
    sys.exit(1)

for _ in range(int(num_lines)):
    input_str: Optional[str] = input_with_timeout("Enter email: ", 60)

    if input_str is None:
        continue

    match: Optional[re.Match[str]] = re.fullmatch(r"^\w+[\w.]*@\w+\.\w{2,6}$"
                                                  , input_str)
    if match:
        print(f'{input_str} is a valid email.')
    else:
        print("Invalid email format.")

if __name__ == "__main__":
    main()
