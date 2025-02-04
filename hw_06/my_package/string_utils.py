from logger import write_log


def to_uppercase(s: str) -> str:
    """
    Converts the given string to uppercase.

    Args:
        s (str): The input string.

    Returns:
        str: The input string converted to uppercase.
    """
    write_log(f"to_uppercase called with argument '{s}'")

    return s.upper()


def strip_spaces(s: str) -> str:
    """
    Removes leading and trailing whitespace from the given string.

    Args:
        s (str): The input string.

    Returns:
        str: The input string with leading and trailing spaces removed.
    """
    write_log(f"to_uppercase called with argument '{s}'")

    return s.strip()
