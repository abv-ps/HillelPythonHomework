class MutableClass:
    """
    A class that allows dynamic addition and removal of attributes at runtime.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of MutableClass.
        """
        pass

    def add_attribute(self, name: str, value: object) -> None:
        """
        Adds a new attribute to the instance.

        Args:
            name (str): The name of the attribute to add.
            value (object): The value to assign to the attribute.
        """
        setattr(self, name, value)

    def remove_attribute(self, name: str) -> None:
        """
        Removes an attribute from the instance if it exists.

        Args:
            name (str): The name of the attribute to remove.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        if hasattr(self, name):
            delattr(self, name)
        else:
            raise AttributeError(f"The object has no attribute with the name '{name}'")

if __name__ == "__main__":
    obj = MutableClass()

    obj.add_attribute("name", "Python")
    print(obj.name)  # Output: Python

    obj.remove_attribute("name")
    try:
        print(obj.name)  # An error occurs, the attribute is deleted
    except AttributeError as e:
        print(e)
