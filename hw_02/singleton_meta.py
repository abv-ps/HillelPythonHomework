from typing import Any, Dict


class SingletonMeta(type):
    """
    A metaclass for implementing the Singleton  pattern.

    Attributes:
        _instances (Dict[type, Any]): Dictionary that stores only the single instance of each class.
    """

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args: Any) -> Any:
        """
        Override the __call__ method to ensure only one instance of the class is created.

        Args:
            *args (Any): Positional arguments for the class constructor.
            **kwargs (Any): Keyword arguments for the class constructor.

        Returns:
            Any: The single instance of the class.
        """
        if cls not in cls._instances:
            # If an instance does not exist, create and store it
            instance = super().__call__(*args)
            cls._instances[cls] = instance
            print("Creating instance")
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    A class that uses SingletonMeta as its metaclass to ensure a single instance.

    Methods:
        __init__(self): Initializes the Singleton instance.
    """

    def __init__(self) -> None:
        pass


# Example usage:
if __name__ == "__main__":
    obj1 = Singleton()  # Create the first instance
    obj2 = Singleton()  # Attempt to create another instance, should return the same instance

    print(obj1 is obj2)  # Check if both variables reference the same object (should print True)
