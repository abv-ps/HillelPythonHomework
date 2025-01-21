import inspect
from typing import Any


def is_callable_obj(obj: Any) -> None:
    """
    Lists all callable methods and functions of the given object.

    Outputs those attributes that are methods of a class or functions
    of a module.

    Parameters:
        obj (Any): The object to inspect.

    Returns:
        None: Prints the list of callable methods or functions of the object.
    of a module.
    """
    all_methods = []

    # For classes or objects, check for methods
    if inspect.isclass(obj):
        all_methods = [attr for attr in dir(obj) if inspect.ismethod(getattr(obj, attr))]
    # For modules or functions, check for functions
    else:
        all_methods = [attr for attr in dir(obj) if inspect.isfunction(getattr(obj, attr))]

    print(f"\nAll callable methods belonging to the '{type(obj).__name__}':")
    if all_methods:
        print(", ".join(all_methods))
    else:
        print("No callable methods found.")


def call_function(obj: Any, method_name: str, *args: Any) -> Any:
    """
    Calls a method of the given object with the specified arguments.

    Parameters:
        obj (Any): The object containing the method.
        method_name (str): The name of the method to call.
        *args (Any): Arguments to pass to the method.

    Returns:
        Any: The result of the method call.

    Raises:
        AttributeError: If the method does not exist.
        TypeError: If the attribute is not callable or arguments do not match the method's signature.
    """
    # Check if the method exists
    if not hasattr(obj, method_name):
        raise AttributeError(
            f"'{type(obj).__name__}' object has no attribute '{method_name}'"
        )

    method = getattr(obj, method_name)

    if not callable(method):
        raise TypeError(
            f"'{method_name}' is not a callable method of {type(obj).__name__}"
        )

    return method(*args)


class Calculator:
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
    calc = Calculator()
    is_callable_obj(calc)
    print(call_function(calc, "add", 10, 5))  # 15
    print(call_function(calc, "subtract", 10, 5))  # 5
