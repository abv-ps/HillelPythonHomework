from math import pi


def calculate_circle_area(radius: float) -> float:
    """
    Calculate the area of a circle.

    Args:
        radius (float): The radius of the circle. Must be a positive number.

    Returns:
        float: The area of the circle, calculated as π * radius^2.
    """
    return pi * radius ** 2


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


# execute only in this file
if __name__ == "__main__":
    # Request radius from the user
    r = input('Enter the radius of circle (positive number): ')

    if is_number(r):
        r = float(r)
        if r > 0:
            print('The area of the circle is: ', calculate_circle_area(r))
        else:
            print('Radius of the circle must be a positive number.')
    else:
        print('Radius of the circle must be a positive number.')
