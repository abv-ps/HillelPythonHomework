"""
This module provides a function for division with exception handling.

Functions:
- divide(a: int, b: int) -> float: Divides two integers and handles division by zero.

Unit tests are implemented using pytest.

To run the tests, use:
    pytest <filename>.py
"""

import pytest


def divide(a: int, b: int) -> float:
    """
    Divides two integers and returns the result.

    Args:
        a (int): The numerator.
        b (int): The denominator.

    Returns:
        float: The result of division.

    Raises:
        ZeroDivisionError: If the denominator is zero.

    Examples:
        >>> divide(10, 2)
        5.0
        >>> divide(9, 3)
        3.0
        >>> divide(7, 2)
        3.5
        >>> divide(10, 0)
        Traceback (most recent call last):
        ZeroDivisionError: Division by zero is not allowed.
    """
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b


# Unit tests for the divide function

def test_divide_correct():
    """Test valid division results."""
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0
    assert divide(7, 2) == 3.5


def test_divide_zero_division():
    """Test if function raises ZeroDivisionError when dividing by zero."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (9, 3, 3.0),
    (7, 2, 3.5),
    (100, 4, 25.0),
    (20, 5, 4.0)
])
def test_divide_parametrized(a: int, b: int, expected: float):
    """Parameterized test for different division cases."""
    assert divide(a, b) == expected
