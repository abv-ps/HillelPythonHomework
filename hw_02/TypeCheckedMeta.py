from typing import Any, Dict, Type


class TypeCheckedMeta(type):
    """
    A metaclass that enforces type checking for class and instance attributes when they are set.

    Attributes with type annotations will be checked, and if the value assigned to
    the attribute does not match the specified type, a TypeError will be raised.
    """

    def __new__(cls: type, name: str, bases: tuple, dct: Dict[str, Any]) -> type:
        """
        Create a new class and store type annotations for attributes.

        Args:
            cls (type): The metaclass.
            name (str): The name of the class being created.
            bases (tuple): Base classes of the class being created.
            dct (Dict[str, Any]): Dictionary of attributes for the new class.

        Returns:
            type: The newly created class.
        """
        annotations = dct.get('__annotations__', {})

        # Add __setattr__ for instance-level type checking
        def instance_setattr(self, name: str, value: Any) -> None:
            expected_type = getattr(self, '_type_annotations', {}).get(name, None)
            if expected_type and not isinstance(value, expected_type):
                raise TypeError(
                    f"For attribute '{name}' expected tipe is '{expected_type.__name__}', "
                    f"but now the type is '{type(value).__name__}'."
                )
            super(self.__class__, self).__setattr__(name, value)

        dct['__setattr__'] = instance_setattr
        cls_obj = super().__new__(cls, name, bases, dct)
        cls_obj._type_annotations = annotations
        return cls_obj


class Person(metaclass=TypeCheckedMeta):
    name: str = ""
    age: int = 0


# Example usage
if __name__ == "__main__":
    p = Person()
    p.name = "John"  # All good
    print(p.name)
    p.age = '30'  # Raises TypeError

