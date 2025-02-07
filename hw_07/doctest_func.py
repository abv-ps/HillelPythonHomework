"""
This module provides basic mathematical functions for working with numbers.

Functions:
- is_even(n: int) -> bool: Checks if a number is even.
- factorial(n: int) -> int: Computes the factorial of a given number.

Each function includes doctest examples. To run the tests, execute:

    python -m doctest <filename>.py -v
"""


def is_even(n: int) -> bool:
    """
    Checks if a given number is even.

    Args:
        n (int): The integer number to check.

    Returns:
        bool: True if the number is even, otherwise False.

    Examples:
        >>> is_even(2)
        True
        >>> is_even(3)
        False
        >>> is_even(0)
        True
        >>> is_even(-4)
        True
        >>> is_even(-5)
        False
    """
    return n % 2 == 0


def factorial(n: int) -> int:
    """
    Computes the factorial of a given number.

    Args:
        n (int): A non-negative integer.

    Returns:
        int: The factorial of the number.

    Raises:
        ValueError: If n is negative.

    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
        >>> factorial(1)
        1
        >>> factorial(4)
        24
        >>> factorial(7)
        5040
        >>> factorial(-3)
        Traceback (most recent call last):
        ValueError: Factorial is not defined for negative numbers
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
