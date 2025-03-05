"""
This module provides a decorator function `log_wrapper` for logging method calls
and responses in a class. The decorator wraps each method of the given class and logs
the method name, its arguments, keyword arguments, and the response status and body.

The module aims to facilitate debugging, auditing, or monitoring of method calls
by capturing detailed information about the method invocation and its response.

Functions:
    log_wrapper(cls: type) -> type:
        A decorator for logging calls to class methods. It wraps the methods of a
        class and logs the method calls along with their arguments, keyword arguments,
        HTTP status, and response body.

Classes:
    None

Exceptions:
    None

Usage:
    To use the decorator, simply apply it to a class definition. All methods within
    the class will be automatically wrapped to log their invocations.
"""
import logging
from typing import Any, Callable


def log_wrapper(cls: type) -> type:
    """
    Decorator for logging calls to class methods. This decorator wraps
    each method of the given class, logging the method calls along
    with their arguments, keyword arguments, and the server's response.

    Args:
        cls (type): The class whose methods will be wrapped for logging.

    Returns:
        type: The same class with wrapped methods that log method calls.
    """

    def wrap_method(name: str, method: Callable) -> Callable:
        """
        Create a wrapper for a method to log its calls. This function
        wraps the original method and logs the arguments, keyword arguments,
        HTTP status, and response body.

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
            logging.info(f"{name} called with args: {args}, kwargs: {kwargs}")

            response = method(self, *args, **kwargs)

            status = self._status_code
            response_body = self._response_body

            logging.info(f"Response Status: {status}")
            logging.info(f"Response Body: {response_body}")

            return response

        return wrapped_method

    # Wrapper for all methods of class
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, wrap_method(name, method))

    return cls
