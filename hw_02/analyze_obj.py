from typing import Any


def analyze_object(val: Any) -> None:
    """
    Analyzes an object and prints:
    - Type of the object.
    - List of all attributes and methods.
    - Type of each attribute or method.

    Parameters:
        val (Any): The object to analyze.
    """
    print("Type of object:", type(val))
    print("\nAttributes and methods:")
    for attr in dir(val):
        try:
            # Create the variable to avoid calling getattr twice
            attr_value = getattr(val, attr)
            print(f"- {attr}: {type(attr_value)}")
        except Exception as err:
            print(f"Error retrieving attribute {attr}: {err}")


class MyClass:
    """
    Represents a greeting interaction that generates a personalized greeting message.

    Attributes:
        value (str): The value used to personalize the greeting message.

    Methods:
        __init__(self, value): Initializes the object with a given value.
        say_hello(self): Returns a personalized greeting message in the format "Hello, {value}",
                         where 'value' is the attribute assigned during initialization.
    """

    def __init__(self, value: str) -> None:
        """
        Initializes the object with the provided value to be used in the greeting message.

        Parameters:
            value (str): The value used to personalize the greeting message.
        """
        self.value = value

    def say_hello(self) -> str:
        """
        Returns a personalized greeting message in the format "Hello, {value}",
        where 'value' is the attribute assigned during initialization.

        Returns:
            str: A greeting message.
        """
        return f"Hello, {self.value}"


if __name__ == "__main__":
    obj = MyClass("World")
    analyze_object(obj)
