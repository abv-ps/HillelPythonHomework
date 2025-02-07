"""
Module for age verification.

This module provides a class for checking if a user is an adult based on their age.
It includes unit tests with skips and conditions.
"""
from typing import Any
import pytest


class AgeVerifier:
    """
    A class to verify if a given age qualifies as adult.
    """

    @staticmethod
    def is_adult(age: int) -> bool:
        """
        Checks if the given age is 18 or older.

        Args:
            age (int): The age to check.

        Returns:
            bool: True if age is 18 or older, False otherwise.

        Examples:
            >>> AgeVerifier.is_adult(18)
            True

            >>> AgeVerifier.is_adult(17)
            False
        """
        return age >= 18


@pytest.mark.parametrize("age, expected", [
    (17, False),
    (18, True),
    (21, True),
    (0, False),
])
def test_is_adult(age: int, expected: bool) -> None:
    assert AgeVerifier.is_adult(age) == expected


@pytest.mark.skip(reason="Invalid age value")
def test_negative_age() -> None:
    assert not AgeVerifier.is_adult(-5)


@pytest.mark.skipif(121 > 120, reason="Unlikely age value")
def test_unrealistic_age() -> None:
    assert not AgeVerifier.is_adult(121)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
