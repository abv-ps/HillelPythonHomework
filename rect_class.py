import random
from calc_circ_area import is_number  # Custom function for checking if a value is a number

# Global variables for testing rectangle size changes
old_width = None
old_height = None


class Rectangle:
    """
    The class describes a rectangle with a given height and width.

    The class provides the following methods:
        - __init__(self, width, height): Constructor that accepts the width and height of the rectangle.
        - area(self): Returns the area of the rectangle.
        - perimeter(self): Returns the perimeter of the rectangle.
        - is_square(self): Returns True if the rectangle is a square (width equals height), False otherwise.
        - resize(self, new_width, new_height): Changes the width and height of the rectangle by taking new values.
    """

    def __init__(self, width: float, height: float):
        """Initialize the rectangle with a given width and height."""
        self.width = width
        self.height = height

    def area(self) -> float:
        """Return the area of the rectangle."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Return the perimeter of the rectangle."""
        return 2 * (self.width + self.height)

    def is_square(self) -> bool:
        """Return True if the rectangle is a square, False otherwise."""
        return self.width == self.height

    def resize(self, new_width: float, new_height: float):
        """
        Resize the rectangle by changing its width and height.

        Args:
            new_width (float): The new width of the rectangle.
            new_height (float): The new height of the rectangle.
        """
        global old_width, old_height
        old_width = self.width
        old_height = self.height
        self.width = new_width
        self.height = new_height


def test_func(func, calculating, *args):
    """
    Test a function and compare its result with the expected value.

    Args:
        func (Callable): The function to test.
        calculating: The expected result.
        *args: Arguments to pass to the function.
    """
    try:
        result = func(*args)
        if result == calculating:
            print(f"Rectangle {func.__name__} is {result} as expected.")
        else:
            print(f"Something wrong with the function {func.__name__}. Expected: {calculating}, Got: {result}")
    except Exception as err:
        print(f"Some error with the function {func.__name__}: {err}")


if __name__ == "__main__":
    # Request width and height from the user
    wh = input("Enter the width and height of the rectangle (positive numbers separated by a space): ")
    parts = wh.split()

    # Check if input is valid
    if len(parts) == 2 and is_number(parts[0]) and is_number(parts[1]):
        width, height = map(float, parts)

        if width > 0 and height > 0:
            # Create a Rectangle object
            rectangle = Rectangle(width, height)

            # Test all methods
            test_func(rectangle.area, calculating=width * height)
            test_func(rectangle.perimeter, calculating=2 * (width + height))
            test_func(rectangle.is_square, width == height)

            # Test the resize method
            rectangle.resize(float(random.randint(1, 9)), float(random.randint(1, 9)))
            if not (rectangle.width == old_width and rectangle.height == old_height):
                print(f"Old width = {old_width}, After resize width = {rectangle.width}")
                print(f"Old height = {old_height}, After resize height = {rectangle.height}")
            else:
                print(
                    f"Something wrong with the function Resize: "
                    f"expected width = {rectangle.width}, expected height = {rectangle.height}, "
                    f"but got width = {old_width}, height = {old_height}"
                )
        else:
            print("Both width and height must be positive numbers.")
    else:
        print("Invalid input. Please enter two positive numbers separated by a space.")
