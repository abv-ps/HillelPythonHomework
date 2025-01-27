import math
from typing import Union


class Vector:
    """
    A class to represent a 2D vector.

    Args:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
    """

    def __init__(self, x: float, y: float):
        """
        Initialize a vector with x and y coordinates.

        Args:
            x (float): The x-coordinate of the vector.
            y (float): The y-coordinate of the vector.
        """
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        """
        Add two vectors.

        Args:
            other (Vector): The vector to add.

        Returns:
            Vector: A new vector that is the sum of the two vectors.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        """
        Subtract one vector from another.

        Args:
            other (Vector): The vector to subtract.

        Returns:
            Vector: A new vector that is the result of the subtraction.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]) -> "Vector":
        """
        Multiply the vector by a scalar.

        Args:
            scalar (Union[int, float]): The scalar value to multiply by.

        Returns:
            Vector: A new vector that is the result of the multiplication.
        """
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self.x * scalar, self.y * scalar)

    def __lt__(self, other: "Vector") -> bool:
        """
        Compare two vectors by their length (less than).

        Args:
            other (Vector): The vector to compare to.

        Returns:
            bool: True if this vector is shorter than the other, False otherwise.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return self.length() < other.length()

    def __eq__(self, other: "Vector") -> bool:
        """
        Compare two vectors by their length (equality).

        Args:
            other (Vector): The vector to compare to.

        Returns:
            bool: True if both vectors have the same length, False otherwise.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return self.length() == other.length()

    def length(self) -> float:
        """
        Calculate the length (magnitude) of the vector.

        Returns:
            float: The length of the vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self) -> str:
        """
        Represent the vector as a string.

        Returns:
            str: The string representation of the vector in the form '(x, y)'.
        """
        return f"({self.x}, {self.y})"
