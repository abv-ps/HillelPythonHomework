def is_number(value: str) -> bool:
    """
    Check if the given value can be converted to a number.

    Args:
        value (str): The input value to check.

    Returns:
        bool: True if the value can be converted to a float, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_number_val(value: str) -> float | None:
    """
    Checks if the value can be converted to a number.
    If so, returns the converted value, otherwise None.

    Args:
        value (str): The input value to check.

    Returns:
        float | None: A numeric value or None if this is not possible.
    """
    try:
        return float(value)
    except ValueError:
        return None

def is_callable_obj(obj: Any) -> None:
    """
    Lists all callable methods and functions of the given object.

    Outputs those attributes that are methods of a class or functions
    of a module.

    Parameters:
        obj (Any): The object to inspect.

    Returns:
        None: Prints the list of callable methods or functions of the object.
    of a module.
    """
    all_methods = []

    # For classes or objects, check for methods
    if inspect.isclass(obj):
        all_methods = [attr for attr in dir(obj) if inspect.ismethod(getattr(obj, attr))]
    # For modules or functions, check for functions
    else:
        all_methods = [attr for attr in dir(obj) if inspect.isfunction(getattr(obj, attr))]

    print(f"\nAll callable methods belonging to the '{type(obj).__name__}':")
    if all_methods:
        print(", ".join(all_methods))
    else:
        print("No callable methods found.")
