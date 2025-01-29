from typing import Any

class Proxy:
    """
    A proxy class that intercepts attribute access and method calls on the target object.
    """
    def __init__(self, target: Any) -> None:
        """
        Initialize the Proxy with the target object.

        Args:
            target (Any): The object to proxy.
        """
        self._target = target

    def __getattr__(self, name: str) -> Any:
        """
        Intercept attribute access and method calls on the target object.

        Args:
            name (str): The name of the attribute or method to access.

        Returns:
            Any: The attribute or method from the target object. If it is a method,
            it returns a wrapped version that logs calls and arguments.
        """
        # Check if an attribute or method with the same name exists in the target object
        if not hasattr(self._target, name):
            raise AttributeError(f"'{self._target.__class__.__name__}' object has no attribute '{name}'")

        attr = getattr(self._target, name)
        if callable(attr):
            def wrapper(*args: Any) -> Any:
                print(f"Calling method: \n{name} with args: {args}")
                return attr(*args)
            return wrapper
        return attr

class MyClass:
    """
    A simple class with a greet method to demonstrate the Proxy.
    """
    def greet(self, name: str) -> str:
        """
        Return a greeting message.

        Args:
            name (str): The name to include in the greeting.

        Returns:
            str: A greeting message.
        """
        return f"Hello, {name}!"

if __name__ == "__main__":
    obj = MyClass()
    proxy = Proxy(obj)

    # Call the greet method through the proxy
    print(proxy.greet("Alice"))
