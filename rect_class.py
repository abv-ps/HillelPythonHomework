import random

from calc_circ_area import is_number # it is strange that there is no standard function for checking isnumber

# for testing we use global variables to compare them when the rectangle size changes
old_width = None
old_height = None

class Rectangle:
    '''
    The class describes a rectangle with a given height and width.

    The class provide the following methods:

    __init__(self, width, height) — a constructor that accepts the width and height of the rectangle.

    area(self) - a method that returns the area of the rectangle.

    perimeter(self) - a method that returns the perimeter of the rectangle.

    is_square(self) - a method that returns True if the rectangle is a square (width equals height), and False otherwise.

    resize(self, new_width, new_height) - a method that changes the width and height of the rectangle by taking new values.

    '''
    def __init__(self, width, height):
        # initialization the rectangle with a given height and width
        self.width = width
        self.height = height

    def area(self):
        # returns the area of the rectangle
        return self.width * self.height

    def perimeter(self):
        # returns the perimeter of the rectangle
        return 2 * (self.width + self.height)

    def is_square(self):
        # returns the True / False for the statement is the rectangle a square
        return self.width == self.height

    def resize(self, new_width, new_height):
        # use the global variables for further testing
        global old_width, old_height
        old_width = self.width
        old_height = self.height
        # returns the new size of rectangle
        self.width = new_width
        self.height = new_height


def test_func(func, calculating, *args):
    try:
        result = func(*args)  # call the function with arguments
        if result == calculating:
            print("Rectangle", func.__name__, "is", result, "as expected")
        else:
            print("Something wrong with the function", func.__name__, "the calculation should show", result)
    except Exception as err:
        print("Some error with the function", func.__name__, ":", err)

if __name__ == "__main__": # this is a protection against execution in case of import of functions
    # requesting width and height from the user
    wh = input('Enter the width and height of rectangle (positive numbers with a space)): ')

    # splitting the parts of request if user inputs
    parts = wh.split()

    # first check for amount of splitted parts and are they numbers
    if len(parts) == 2 and is_number(parts[0]) and is_number(parts[1]):
        # splitting an input string and converting values to numbers
        width, height = map(float, wh.split())

        # checking the correctness of values
        if width > 0 and height > 0:
            # create an object of the Rectangle class
            rectangle = Rectangle(width, height)

            # test all methods
            test_func(rectangle.area, calculating=width * height)
            test_func(rectangle.perimeter, calculating=2 * (width + height))
            test_func(rectangle.is_square, width == height)
            # for future we can use getattr to promote scalability, and some other ways to get all methods in class to test
            # for resize method need some other approaches
            rectangle.resize(float(random.randint(1, 9)), float(random.randint(1, 9))) # first we randomly resize the rectangle
            if not(rectangle.width == old_width and rectangle.height == old_height):
                print("Old width =", old_width,"\nAfter resize width =", rectangle.width)
                print("Old height =", old_height,"\nAfter resize height =", rectangle.height)
            else:
                print("Something wrong with the function Resize: expected width =", rectangle.width, "expected height =", rectangle.height,
                                        "but got width =", old_width, "height =", old_height)
        else:
            print("Both width and height must be positive numbers.")
    else:
        print("Both width and height must be positive numbers.")