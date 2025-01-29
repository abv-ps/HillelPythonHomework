from typing import Any

class AutoMethodMeta(type):
    """
    A metaclass that automatically generates getter and setter methods
    for each class attribute.

    Generated methods:
    - get_<attribute>() -> Returns the value of the attribute.
    - set_<attribute>(value) -> Sets the value of the attribute.
    """

    def __new__(cls, name: str, bases: tuple, dct: dict) -> type:
        """
        Create a new class and generate getter and setter methods for attributes.

        Args:
            cls (Type[type]): The metaclass.
            name (str): The name of the class being created.
            bases (tuple): Base classes of the class being created.
            dct (dict): Dictionary of attributes for the new class.

        Returns:
            type: The newly created class.
        """
        def make_getter(attr_name: str):
            """Generate a getter method for the given attribute name."""
            def getter(self):
                return getattr(self, f"_{attr_name}")
            return getter

        def make_setter(attr_name: str):
            """Generate a setter method for the given attribute name."""
            def setter(self, value):
                setattr(self, f"_{attr_name}", value)
            return setter

        new_cls = super().__new__(cls, name, bases, dct)

        # Generate getter and setter methods for each attribute in the class dictionary
        for attr_name in dct.keys():
            if not attr_name.startswith("_") and not callable(dct[attr_name]):
                # Add private storage for the attribute
                setattr(new_cls, f"_{attr_name}", dct[attr_name])
                # Add getter
                setattr(new_cls, f"get_{attr_name}", make_getter(attr_name))
                # Add setter
                setattr(new_cls, f"set_{attr_name}", make_setter(attr_name))

        return new_cls

class Person(metaclass=AutoMethodMeta):
    name = "John"
    age = 30

if __name__ == "__main__":
    p = Person()
    print(p.get_name())  # John
    p.set_age(31)
    print(p.get_age())  # 31
