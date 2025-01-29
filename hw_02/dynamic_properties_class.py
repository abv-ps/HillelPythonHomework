from typing import Any


class DynamicProperties:
    """
    A class that allows dynamic addition of properties at runtime using built-in property() function.

    Attributes:
        _properties (dict): Internal dictionary to store property values.
    """

    def __init__(self):
        """Initialize an instance with an empty _properties dictionary."""
        self._properties = {}

    def add_property(self, name: str, default_value: Any) -> None:
        """
        Dynamically add a property with a getter and setter.

        Args:
            name (str): The name of the property to add.
            default_value (Any): The default value of the property.

        Returns:
            None
        """

        def getter(self):
            return self._properties.get(name, default_value)

        def setter(self, value):
            self._properties[name] = value

        # Add the property dynamically
        setattr(self.__class__, name, property(getter, setter))


# Example usage:
if __name__ == "__main__":
    obj = DynamicProperties()

    obj.add_property('name', 'default_name')

    print(obj.name)  # default_name

    obj.name = "Python"

    print(obj.name)  # Python
