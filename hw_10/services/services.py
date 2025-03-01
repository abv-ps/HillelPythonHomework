"""
This module provides functionality for ensuring database cursor availability in class methods.

Key Components:
- `ensure_cursor`: A decorator that ensures a database cursor is available before executing a method.
  If the cursor is unavailable, a `ValueError` is raised.
- `AutoEnsureCursorMeta`: A metaclass that automatically applies the `ensure_cursor` decorator to
  all methods of a class, except for special methods like `__init__`, `__enter__`, and `__exit__`.

Usage:
- The `ensure_cursor` decorator and `AutoEnsureCursorMeta` metaclass work together
  to enforce cursor availability checks for database operations.
"""

from typing import Callable, Any


def ensure_cursor(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that ensures the database cursor is available before executing the function.

    This decorator checks if the 'cursor' attribute exists and is not None. If the cursor
    is unavailable, a ValueError will be raised. If the cursor is available, the decorated
    function is executed.

    Args:
        func (Callable[..., Any]): The function to be decorated. It must take 'self' as its first
                                   argument, and any additional arguments.

    Returns:
        Callable[..., Any]: The wrapped function that checks for cursor availability before
                            execution.

    Raises:
        ValueError: If the database cursor is not available.
    """

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'cursor') or self.cursor is None:
            raise ValueError("Database connection not established.")
        return func(self, *args, **kwargs)

    return wrapper


class AutoEnsureCursorMeta(type):
    """
    A metaclass that automatically applies the ensure_cursor decorator to all methods
    of a class, except for special methods that do not require a database cursor.
    """
    skip_cursor_check_methods = {'__init__', '__enter__', '__exit__'}

    def __new__(mcs, name, bases, dct):
        """
        Creates a new class, applying the ensure_cursor decorator to all methods
        except those in the skip list.

        Args:
            name (str): The name of the class.
            bases (tuple): The base classes of the class.
            dct (dict): The dictionary of class attributes and methods.

        Returns:
            type: The new class with the decorator applied.
        """
        for key, value in dct.items():
            if callable(value) and key not in mcs.skip_cursor_check_methods:
                dct[key] = ensure_cursor(value)  # Apply the decorator to the method
        return super().__new__(mcs, name, bases, dct)
