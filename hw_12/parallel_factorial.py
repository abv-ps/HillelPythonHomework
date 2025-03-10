"""
This module calculates the factorial of a given number using parallel processing.

It divides the task of calculating the factorial into smaller parts, distributing the work
across multiple processes to speed up the computation for large numbers.

Functions:
- partial_factorial: Calculates the factorial for a specific range of numbers.
- parallel_factorial: Calculates the factorial of a number by separating the task
  into several processes.
"""
import multiprocessing


def partial_factorial(start: int, end: int) -> int:
    """
    Calculates the factorial for a part of the range of numbers from start to end.

    Arguments:
    start (int): The starting number of the range.
    end (int): The ending number of the range.

    Returns:
    int: The result of the factorial calculation for the given range.
    """
    result = 1
    for i in range(start, end + 1):
        result *= i
    return result


def parallel_factorial(n: int, num_processes: int) -> int:
    """
   Calculates the factorial of a number n by separating the computation
   between multiple processes.

   Arguments:
   n (int): The number for which the factorial is calculated.
   num_processes (int): The number of processes used for parallel computation.

   Returns:
   int: The factorial of the number n.
   """
    step = n // num_processes
    ranges = [(i * step + 1, (i + 1) * step) for i in range(num_processes)]

    ranges[-1] = (ranges[-1][0], n)

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(partial_factorial, ranges)

    total_factorial = 1
    for result in results:
        total_factorial *= result

    return total_factorial


def main():
    """
    Main function to execute the program.

    It prompts the user to enter a number and the number of processes to use for calculating
    the factorial in parallel, then calculates and prints the factorial.
    """
    n = int(input("Enter a number to calculate the factorial: "))
    num_processes = int(input("Enter the number of processes: "))


    factorial = parallel_factorial(n, num_processes)
    print(f"The factorial of {n} is {factorial}")


if __name__ == "__main__":
    main()
