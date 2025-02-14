"""
This module provides a function to check if a password is secure.

A secure password must:
- Be at least 8 characters long
- Contain at least one digit
- Include at least one uppercase and one lowercase letter
- Have at least one special character (any printable symbol excluding letters and digits)
"""

import re


def secure_password(password: str) -> bool:
    """
    Checks if the given password is secure based on the following criteria:
    - At least 8 characters long
    - Contains at least one digit
    - Includes at least one uppercase and one lowercase letter
    - Has at least one special character (any printable symbol excluding letters and digits)

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password is secure, False otherwise.

    Example:
        >>> secure_password("ТакийСобіПароль")
        False
        >>> secure_password("Непоганий@73")
        True
        >>> secure_password("Неповний73")
        False
        >>> secure_password("сУперП@роль!8")
        True
        >>> secure_password("Sh@rt!7")
        False
    """
    pattern = (r'^(?=.*[a-zа-яіїёєґ])(?=.*[A-ZА-ЯІЇЁЄҐ])(?=.*\d)(?=.*[^\w\d\s])'
               r'[A-Za-zА-Яа-яІіЇїЄєҐґЁёЄєҐґ0-9\W]{8,}$')

    return bool(re.match(pattern, password))


# Example usage
passwords = ["WeakPass", "Strong@123", "NoSpecial123", "short1@A", "Valid$Pass1!", "P@$$w0rd!"]
for pwd in passwords:
    print(f"{pwd}: {secure_password(pwd)}")
