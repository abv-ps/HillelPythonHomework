from typing import Any, Dict


class LimitedAttributesMeta(type):
    """
    A metaclass that restricts the number of attributes a class can have.

    Attributes:
        None
    Methods:
        __new__(cls, name, bases, dct): Ensures the class being created has at most 3 attributes.
    """

    def __new__(cls: type, name: str, bases: tuple, dct: Dict[str, Any]) -> type:
        """
        Create a new class with limited attributes.

        Args:
            name (str): The name of the class being created.
            bases (tuple): The base classes of the class being created.
            dct (Dict[str, Any]): The dictionary of class attributes.

        Returns:
            type: The newly created class.

        Raises:
            TypeError: If the class has more than 3 non-dunder attributes.
        """
        # Count non-dunder attributes
        non_dunder_attrs = [key for key in dct if not key.startswith('__')]
        if len(non_dunder_attrs) > 3:
            raise TypeError(f"Class '{name}' cannot have more than 3 attributes.")
        return super().__new__(cls, name, bases, dct)

class LimitedClass(metaclass=LimitedAttributesMeta):
    """
    A class with a limit of 3 attributes enforced by LimitedAttributesMeta.

    Attributes:
        attr1 (int): An example attribute.
        attr2 (int): An example attribute.
        attr3 (int): An example attribute.
    """

    attr1 = 1
    attr2 = 2
    attr3 = 3
    attr4 = 4  # This will cause an error due to exceeding the attribute limit.

# Example usage
if __name__ == "__main__":
    # Creating an instance of LimitedClass
    obj = LimitedClass()
    print(obj.attr1)  # Outputs: 1
