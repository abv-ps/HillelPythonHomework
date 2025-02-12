"""
This module provides a decorator for logging method calls of a class. The decorator
wraps each method of the class and logs the method name, its arguments, and keyword
arguments every time the method is called. This is useful for debugging, tracking,
or auditing method invocations.

Functions:
    log_wrapper(cls: type) -> type:
        A decorator for logging calls to class methods, wrapping each method with
        logging functionality.

Example:
    @log_wrapper
    class MyClass:
        def add(self, a: int, b: int) -> int:
            return a + b

    obj = MyClass()
    obj.add(5, 3)  # Logs: add called with args: (5, 3), kwargs: {}
"""

from typing import Any, Callable


def log_wrapper(cls: type) -> type:
    """
    Decorator for logging calls to class methods. This decorator wraps
    each method of the given class, logging the method calls along
    with their arguments and keyword arguments.

    Args:
        cls (type): The class whose methods will be wrapped for logging.

    Returns:
        type: The same class with wrapped methods that log method calls.

    Example:
        @log_wrapper
        class MyClass:
            def add(self, a: int, b: int) -> int:
                return a + b

        obj = MyClass()
        obj.add(5, 3)  # Logs: add called with args: (5, 3), kwargs: {}
    """

    def wrap_method(name: str, method: Callable) -> Callable:
        """
        Create a wrapper for a method to log its calls. This function
        wraps the original method and logs the arguments and keyword
        arguments passed to it.

        Args:
            name (str): The name of the method to be wrapped.
            method (Callable): The original method that will be wrapped.

        Returns:
            Callable: The wrapped method which logs calls before invoking the original method.
        """

        def wrapped_method(self: Any, *args: Any, **kwargs: Any) -> None:
            """
            Logs method calls and then invokes the original method.

            Args:
                self (Any): The instance of the class.
                *args (Any): Positional arguments passed to the method.
                **kwargs (Any): Keyword arguments passed to the method.
            """
            print(f"Logging: {name} called with args: {args}, kwargs: {kwargs}")
            return method(self, *args, **kwargs)

        return wrapped_method

    # Wrap all methods in the class
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, wrap_method(name, method))

    return cls
