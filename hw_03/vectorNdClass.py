from math import sqrt


class Vector:
    """
    Represents an n-dimensional vector with basic vector operations.
    """

    def __init__(self, *components: float):
        """
        Initializes a vector with n dimensions.

        Args:
            components (float): Coordinates of the vector in n-dimensional space.
        """
        self.components = list(components)

    def __add__(self, other: "Vector") -> "Vector":
        """
        Adds two vectors.

        Args:
            other (Vector): Another vector to add.

        Returns:
            Vector: The resulting vector after addition.

        Raises:
            ValueError: If the dimensions of the vectors do not match.
        """
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for addition.")
        return Vector(*(self.components[i] + other.components[i] for i in range(len(self.components))))

    def __sub__(self, other: "Vector") -> "Vector":
        """
        Subtracts another vector from this vector.

        Args:
            other (Vector): Another vector to subtract.

        Returns:
            Vector: The resulting vector after subtraction.

        Raises:
            ValueError: If the dimensions of the vectors do not match.
        """
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for subtraction.")
        return Vector(*(self.components[i] - other.components[i] for i in range(len(self.components))))

    def __mul__(self, other: "Vector") -> float:
        """
        Calculates the multiplication of two vectors.

        Args:
            other (Vector): Another vector for the multiplication.

        Returns:
            float: The resulting scalar value from the multiplication.

        Raises:
            ValueError: If the dimensions of the vectors do not match.
        """
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for scalar multiplication.")
        return sum(self.components[i] * other.components[i] for i in range(len(self.components)))

    def length(self) -> float:
        """
        Calculates the length (modulus) of a vector.

        Returns:
            float: The length of the vector.
        """
        return sqrt(sum(x**2 for x in self.components))

    def __lt__(self, other: "Vector") -> bool:
        """
        Compares the length of this vector with another to determine if it is shorter.

        Args:
            other (Vector): Another vector to compare.

        Returns:
            bool: True if this vector is shorter, False otherwise.
        """
        return self.length() < other.length()

    def __eq__(self, other: "Vector") -> bool:
        """
        Checks if the lengths of two vectors are equal.

        Args:
            other (Vector): Another vector to compare.

        Returns:
            bool: True if the lengths are equal, False otherwise.
        """
        return self.length() == other.length()
