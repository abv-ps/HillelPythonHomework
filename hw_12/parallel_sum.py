"""
Module for calculating the sum of a list of numbers using parallel processing.

This module provides functions for calculating the sum of numbers in a list.
It supports parallel computation by splitting the list into chunks and
computing the sum using multiple processes, which can significantly speed up
the computation for large lists.

Functions:
    partial_sum(numbers: List[int]) -> int:
        Calculates the sum of the given list of numbers.

    parallel_sum(numbers: List[int], num_processes: int) -> int:
        Splits the list into chunks and calculates the sum in parallel using multiple processes.
"""

import multiprocessing
from typing import List


def partial_sum(numbers: List[int]) -> int:
    """
    Calculates the sum of a given list of numbers.

    Args:
        numbers (List[int]): The list of numbers to sum.

    Returns:
        int: The sum of the numbers.
    """
    return sum(numbers)


def parallel_sum(numbers: List[int], num_processes: int) -> int:
    """
    Splits the list into chunks and calculates the sum in parallel.

    Args:
        numbers (List[int]): The list of numbers to sum.
        num_processes (int): The number of processes to use.

    Returns:
        int: The total sum of all numbers.
    """
    chunk_size = len(numbers) // num_processes
    chunks = [numbers[i * chunk_size: (i + 1) * chunk_size] for i in range(num_processes)]

    if len(numbers) % num_processes:
        chunks[-1].extend(numbers[num_processes * chunk_size:])

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(partial_sum, chunks)

    return sum(results)


def main():
    """
    The main function of the program that generates a large array and calculates its sum using parallel processing.

    This function performs the following steps:
    1. Generates a large array (`large_array`) containing 100,000 random integers between 1 and 100.
    2. Specifies the number of worker processes (`num_workers`) to use for parallel processing.
    3. Calls the `parallel_sum()` function to compute the total sum of the array using the specified number of worker processes.
    4. Prints the total sum of the array.

    Returns:
    None
    """
    import random

    large_array = [random.randint(1, 100) for _ in range(100000)]
    num_workers = 4

    total = parallel_sum(large_array, num_workers)
    print(f"Total sum: {total}")


if __name__ == "__main__":
    main()
