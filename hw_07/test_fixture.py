"""
User Management Module

This module provides a `UserManager` class for managing users. It allows adding,
removing, and retrieving users.

Classes:
- UserManager: Manages user records.

Functions:
- add_user(name: str, age: int) -> None: Adds a user to the system.
- remove_user(name: str) -> None: Removes a user by name.
- get_all_users() -> list[dict]: Returns a list of all users.

Unit tests are implemented using pytest with fixtures.

To run the tests, use:
    pytest <filename>.py
"""

import pytest
from typing import List, Dict


class UserManager:
    """Class for managing users."""

    def __init__(self):
        """Initializes an empty user list."""
        self.users: List[Dict[str, int]] = []

    def add_user(self, name: str, age: int) -> None:
        """
        Adds a new user.

        Args:
            name (str): The user's name.
            age (int): The user's age.

        Examples:
            >>> um = UserManager()
            >>> um.add_user("Alice", 30)
            >>> um.get_all_users()
            [{'name': 'Alice', 'age': 30}]
        """
        self.users.append({"name": name, "age": age})

    def remove_user(self, name: str) -> None:
        """
        Removes a user by name.

        Args:
            name (str): The name of the user to remove.

        Examples:
            >>> um = UserManager()
            >>> um.add_user("Alice", 30)
            >>> um.remove_user("Alice")
            >>> um.get_all_users()
            []
        """
        self.users = [user for user in self.users if user["name"] != name]

    def get_all_users(self) -> List[Dict[str, int]]:
        """
        Returns a list of all users.

        Returns:
            list[dict]: A list of dictionaries representing users.

        Examples:
            >>> um = UserManager()
            >>> um.add_user("Alice", 30)
            >>> um.get_all_users()
            [{'name': 'Alice', 'age': 30}]
        """
        return self.users


# Fixture that initializes a UserManager instance with sample data
@pytest.fixture
def user_manager():
    """
    Fixture that initializes a UserManager instance with two users.

    Returns:
        UserManager: A pre-configured instance of UserManager.
    """
    um = UserManager()
    um.add_user("Alice", 30)
    um.add_user("Bob", 25)
    return um


# Tests for UserManager

def test_add_user(user_manager):
    """Tests if a user is correctly added to the manager."""
    user_manager.add_user("Charlie", 35)
    users = user_manager.get_all_users()
    assert len(users) == 3
    assert users[-1] == {"name": "Charlie", "age": 35}


def test_remove_user(user_manager):
    """Tests if a user is correctly removed from the manager."""
    user_manager.remove_user("Alice")
    users = user_manager.get_all_users()
    assert len(users) == 1
    assert users[0] == {"name": "Bob", "age": 25}


def test_get_all_users(user_manager):
    """Tests if all users are correctly retrieved."""
    users = user_manager.get_all_users()
    assert len(users) == 2
    assert {"name": "Alice", "age": 30} in users
    assert {"name": "Bob", "age": 25} in users


@pytest.mark.skipif(
    lambda: len(user_manager().get_all_users()) < 3,
    reason="Not enough users for this test."
)
def test_skip_if_few_users(user_manager):
    """This test is skipped if there are fewer than three users."""
    users = user_manager.get_all_users()
    assert len(users) >= 3
