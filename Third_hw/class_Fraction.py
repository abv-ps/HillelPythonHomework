from math import gcd


class Fraction:
    """
    A class for handling fractions (rational numbers).

    Args:
        numerator (int): The numerator of the fraction.
        denominator (int): The denominator of the fraction.
    """

    def __init__(self, numerator: int, denominator: int):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self.numerator = numerator
        self.denominator = denominator
        self.simplify()

    def simplify(self) -> None:
        """Simplifies a fraction by finding the greatest common divisor (GCD)."""
        common_divisor = gcd(self.numerator, self.denominator)
        self.numerator //= common_divisor
        self.denominator //= common_divisor
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    def __add__(self, other: "Fraction") -> "Fraction":
        """Adding two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented
        new_numerator = (
                self.numerator * other.denominator + other.numerator * self.denominator
        )
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __sub__(self, other: "Fraction") -> "Fraction":
        """Subtracting two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented
        new_numerator = (
                self.numerator * other.denominator - other.numerator * self.denominator
        )
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other: "Fraction") -> "Fraction":
        """Multiplication of two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other: "Fraction") -> "Fraction":
        """Division of two fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented
        if other.numerator == 0:
            raise ValueError("Cannot divide by zero.")
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return Fraction(new_numerator, new_denominator)

    def __eq__(self, other: "Fraction") -> bool:
        """Check for equality of fractions."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return (
                self.numerator == other.numerator
                and self.denominator == other.denominator
        )

    def __repr__(self) -> str:
        """Correct representation of a fraction in the form 'numerator/denominator'."""
        return f"{self.numerator}/{self.denominator}"
