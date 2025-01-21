import inspect

def analyze_inheritance(cls: type) -> None:
    """
    Analyze the inheritance of a class and list all methods inherited from its base classes.

    Args:
        cls (type): The class to analyze.

    Returns:
        None
    """
    # Get the list of base classes (parents)
    parents = cls.__bases__

    # Avoid duplication of methods
    inherited_methods = set()

    # Iterate over each base class
    for parent in parents:
        # Get methods of the base class
        for name, method in inspect.getmembers(parent, inspect.isfunction):
            # Check if the method is not overridden in the child class
            if name not in cls.__dict__:
                inherited_methods.add((name, parent.__name__))

    # Output inherited methods
    print(f"Class {cls.__name__} inherits:")
    if inherited_methods:
        for method_name, parent_name in inherited_methods:
            print(f"- {method_name} from {parent_name}")
    else:
        print("No methods inherited from base classes.")

# Example usage
class Parent:
    def parent_method(self):
        pass

class Child(Parent):
    def child_method(self):
        pass

# Analyze inheritance of the Child class
analyze_inheritance(Child)
