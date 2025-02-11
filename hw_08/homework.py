"""
Utility Functions Module

This module provides a collection of utility functions for performing common operations,
such as calculating discounts, filtering adults from a list, parsing input values,
and applying operations to numbers using higher-order functions.

Features:
- `calculate_discount`: Computes a discounted price.
- `filter_adults`: Filters a list of people based on age.
- `parse_input`: Parses an integer from a string or returns the original integer.
- `get_first`: Retrieves the first element of a list.
- `apply_operation`: Applies a mathematical operation to a number using a callable.

Usage:
These functions are useful for handling pricing, data filtering, input parsing,
and functional programming operations.
"""
import doctest
from typing import Union, Optional, TypeVar, Callable

T = TypeVar('T')


def calculate_discount(price: float, discount: float) -> float:
    """
    Calculates the discounted price based on a given percentage.

    Args:
        price (float): The original price.
        discount (float): The discount percentage.

    Returns:
        float: The final price after applying the discount.
        If the discount is greater than 100%, returns 0.

    Examples:
        >>> calculate_discount(100, 20)
        80.0
        >>> calculate_discount(50, 110)
        0.0
        >>> calculate_discount(175, 0)
        175.0
    """
    if discount > 100:
        return 0.0
    return price - (price * (discount / 100))


def filter_adults(people: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    Filters a list of people to include only adults (18+ years old).

    Args:
        people (list[tuple[str, int]]): A list of tuples where each tuple contains a name and an age.

    Returns:
        list[tuple[str, int]]: A list containing only adults.

    Examples:
        >>> filter_adults([("Андрій", 25), ("Олег", 16), ("Марія", 19), ("Ірина", 15)])
        [('Андрій', 25), ('Марія', 19)]
        >>> filter_adults([("Іван", 30), ("Анна", 17)])
        [('Іван', 30)]
        >>> filter_adults([("Олег", 16)])
        []
    """
    return [person for person in people if person[1] >= 18]


def parse_input(value: Union[int, str]) -> int | None:
    """
    Parses an integer from a given input, which may be a string or an integer.

    Args:
        value (Union[int, str]): The input value to parse.

    Returns:
        Optional[int]: The parsed integer, or None if parsing fails.

    Examples:
        >>> parse_input(37)
        37
        >>> parse_input("99")
        99
        >>> parse_input("Привіт") is None
        True
    """
    if isinstance(value, int):
        return value
    elif isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def get_first(elements: list[T]) -> Optional[T]:
    """
    Retrieves the first element from a list.

    Args:
        elements (list[T]): A list of elements of any type.

    Returns:
        Optional[T]: The first element if the list is not empty, otherwise None.

    Examples:
        >>> get_first([1, 2, 3])
        1
        >>> get_first(["a", "b", "c"])
        'a'
        >>> get_first([]) is None
        True
    """
    return elements[0] if elements else None


def square() -> Callable[[int], int]:
    """
    Returns a function that calculates the square of a number.

    Returns:
        Callable[[int], int]: A function that squares an integer.

    Examples:
        >>> square()(3)
        9
        >>> square()(5)
        25
    """
    return lambda x: x * x


def double() -> Callable[[int], int]:
    """
    Returns a function that doubles a number.

    Returns:
        Callable[[int], int]: A function that doubles an integer.

    Examples:
        >>> double()(3)
        6
        >>> double()(5)
        10
    """
    return lambda x: x * 2


def apply_operation(x: int, operation: Callable[[int], int]) -> int:
    """
    Applies a given operation to an integer.

    Args:
        x (int): The input integer.
        operation (Callable[[int], int]): A function that takes an integer and returns an integer.

    Returns:
        int: The result of applying the operation to x.

    Examples:
        >>> apply_operation(3, square())
        9
        >>> apply_operation(5, double())
        10
    """
    return operation(x)


if __name__ == "__main__":
    doctest.testmod()
    print(calculate_discount(100, 20))  # 80.0
    print(calculate_discount(50, 110))  # 0.0

    people = [("Андрій", 25), ("Олег", 16), ("Марія", 19), ("Ірина", 15)]
    print(filter_adults(people))  # [('Андрій', 25), ('Марія', 19)]

    print(parse_input(42))  # 42
    print(parse_input("100"))  # 100
    print(parse_input("hello"))  # None

    print(get_first([1, 2, 3]))  # 1
    print(get_first(["a", "b", "c"]))  # 'a'
    print(get_first([]))  # None

    print(apply_operation(5, square()))  # 25
    print(apply_operation(5, double()))  # 10

