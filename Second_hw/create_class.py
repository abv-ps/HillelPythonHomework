from typing import Any, Dict

def create_class(class_name: str, methods: Dict[str, Any]) -> type:
    """
    Dynamically creates a class with the specified name and methods.

    Args:
        class_name (str): The name of the class to be created.
        methods (Dict[str, Any]): A dictionary of method names and their corresponding functions.

    Returns:
        type: The dynamically created class.
    """
    return type(class_name, (object,), methods)

def say_hello(self) -> str:
    """
    A method that returns a greeting message.

    Returns:
        str: The greeting message "Hello!".
    """
    return "Hello!"

def say_goodbye(self) -> str:
    """
    A method that returns a farewell message.

    Returns:
        str: The farewell message "Goodbye!".
    """
    return "Goodbye!"

methods = {
    "say_hello": say_hello,
    "say_goodbye": say_goodbye
}

MyDynamicClass = create_class("MyDynamicClass", methods)

if __name__ == "__main__":
    obj = MyDynamicClass()
    print(obj.say_hello())  # Hello!
    print(obj.say_goodbye())  # Goodbye!
