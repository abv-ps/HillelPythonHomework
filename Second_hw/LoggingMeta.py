from typing import Any


class LoggingMeta(type):
    """
    A metaclass that adds logging for attribute access and modification.

    Attributes:
        Any access or modification of attributes in classes using this metaclass
        will be logged to the console.
    """

    def __new__(cls: type, name: str, bases: tuple, dct: dict) -> type:
        """
        Create a new class and add logging to attribute access and modification.

        Args:
            cls (Type[type]): The metaclass.
            name (str): The name of the class being created.
            bases (tuple): Base classes of the class being created.
            dct (dict): Dictionary of attributes for the new class.

        Returns:
            type: The newly created class.
        """
        new_cls = super().__new__(cls, name, bases, dct)
        return new_cls

    def __init__(cls, name: str, bases: tuple, dct: dict) -> None:
        """
        Initialize the class and wrap attribute access and modification methods.

        Args:
            name (str): The name of the class.
            bases (tuple): Base classes of the class.
            dct (dict): Dictionary of attributes for the class.
        """
        super().__init__(name, bases, dct)

        original_getattribute = cls.__getattribute__
        original_setattr = cls.__setattr__

        def logging_getattribute(self, attr: str) -> Any:
            print(f"Logging: accessed '{attr}'")
            return original_getattribute(self, attr)

        def logging_setattr(self, name: str, value: Any) -> None:
            print(f"Logging: modified '{name}'")
            original_setattr(self, name, value)

        cls.__getattribute__ = logging_getattribute
        cls.__setattr__ = logging_setattr


class MyClass(metaclass=LoggingMeta):
    """
    A sample class using the LoggingMeta metaclass.

    Attributes:
        name (str): The name attribute.
    """

    def __init__(self, name: str):
        self.name = name


# Example usage
if __name__ == "__main__":
    obj = MyClass("Python")       # Logging: modified attribute 'name' with value 'Python'
    print(obj.name)               # Logging: accessed attribute 'name'
    obj.name = "New Python"       # Logging: modified attribute 'name' with value 'New Python'
    print(obj.name)               # Logging: accessed attribute 'name'
