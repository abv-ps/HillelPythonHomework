def is_number(value: str) -> float | None:
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
