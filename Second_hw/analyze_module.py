import inspect
import importlib
from typing import Optional

def analyze_module(module_name: str) -> None:
    """
    Analyzes a specified Python module and prints information about its functions
    and classes, including their signatures and parameters.

    Args:
        module_name (str): The name of the module to analyze.

    Returns:
        None: Outputs the analysis results to the console.
    """
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Module '{module_name}' not found.")
        return

    # Output all functions with their signatures and parameter annotations
    functions = [obj for name, obj in inspect.getmembers(module, inspect.isroutine)]

    if functions:
        print("Functions:")
        for name, obj in inspect.getmembers(module, inspect.isroutine):
            try:
                signature = inspect.signature(obj)
                cleaned_params = ', '.join(
                    param.name for param in signature.parameters.values() if param.default == inspect.Parameter.empty
                )
                print(f"- {name}({cleaned_params})")
            except ValueError:
                print(f"- {name}()")
    else:
        print("No functions found.")

    # Output all classes with their signatures
    classes = [obj for name, obj in inspect.getmembers(module, inspect.isclass) if not name.startswith('__')]
    if classes:
        print(f"\nClasses in module '{module_name}':")
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if not name.startswith('__'):
                print(f"  Class: {name}")
                try:
                    signature = str(inspect.signature(obj))
                    print(f"    Signature: {signature}")
                except ValueError:
                    print("    Signature: Unable to retrieve")
    else:
        print(f"\nModule '{module_name}' has no classes.")

if __name__ == "__main__":
    module_name: str = input("Input module name: ")
    analyze_module(module_name)
