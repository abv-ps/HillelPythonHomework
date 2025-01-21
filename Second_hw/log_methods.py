from typing import Any, Callable


def log_methods(cls: type) -> type:
    """
    Decorator for logging calls to class methods.

    Args:
        cls (Type): The class whose methods will be wrapped for logging.

    Returns:
        Type: The same class with wrapped methods.
    """

    def wrap_method(name: str, method: Callable) -> Callable:
        """
        Create a wrapper for a method to log its calls.

        Args:
            name (str): The name of the method.
            method (Callable): The original method to wrap.

        Returns:
            Callable: The wrapped method.
        """

        def wrapped_method(self: Any, *args: Any) -> None:
            """Logs method calls and executes the original method."""
            print(f"Logging: {name} called with {args}")
            method(self, *args)

        return wrapped_method

    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, wrap_method(name, method))
    return cls


@log_methods
class MyClass:
    """
    A class for performing basic math operations.

    Methods:
        add(self, a: int, b: int) -> int: Adds two numbers.
        subtract(self, a: int, b: int) -> int: Subtracts the second number from the first.
    """

    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b

if __name__ == "__main__":
    obj = MyClass()
    obj.add(5, 3)  # Logging: add called with args: (5, 3)
    obj.subtract(5, 3)  # Logging: subtract called with args: (5, 3)