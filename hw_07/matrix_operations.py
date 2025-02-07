"""
Module for matrix operations.

This module provides functions for basic matrix operations such as multiplication
and transposition. It includes doctests for verification.
"""
from typing import List


def matrix_multiply(matrix1: List[List[int]], matrix2: List[List[int]]) -> List[List[int]]:
    """
    Multiplies two matrices.

    Args:
        matrix1 (List[List[int]]): The first matrix.
        matrix2 (List[List[int]]): The second matrix.

    Returns:
        List[List[int]]: The product of the two matrices.

    Raises:
        ValueError: If matrices cannot be multiplied due to incompatible dimensions.

    Examples:
        >>> matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        [[19, 22], [43, 50]]

        >>> matrix_multiply([[2, 3, 4], [1, 0, 0]], [[0, 1000], [1, 100], [0, 10]])
        [[3, 2340], [0, 1000]]
    """
    if len(matrix1[0]) != len(matrix2):
        raise ValueError(
            "Number of columns in the first matrix must be equal to the number of rows in the second matrix.")

    result = [[sum(a * b for a, b in zip(row, col)) for col in zip(*matrix2)] for row in matrix1]
    return result


def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Transposes a given matrix.

    Args:
        matrix (List[List[int]]): The matrix to be transposed.

    Returns:
        List[List[int]]: The transposed matrix.

    Examples:
        >>> transpose_matrix([[1, 2], [3, 4]])
        [[1, 3], [2, 4]]

        >>> transpose_matrix([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]

        >>> transpose_matrix([[1], [2], [3]])
        [[1, 2, 3]]
    """
    return list(map(list, zip(*matrix)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
