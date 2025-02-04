from logger import write_log


def factorial(n: int) -> int:
    """
    Calculates the factorial of a number n.

    Args:
        n (int): The number for which the factorial is calculated.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is negative.

    """
    write_log(f"factorial called with argument {n}")

    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


def gcd(a: int, b: int) -> int:
    """
    Finds the greatest common divisor (GCD) of two numbers a and b.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The GCD of a and b.
    """
    write_log(f"gcd called with arguments {a}, {b}")

    while b:
        a, b = b, a % b
    return a
