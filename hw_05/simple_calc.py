"""Simple mathematical calculator."""

class UnknownOperationError(Exception):
    """Exception raised for unknown arithmetic operations."""



def simple_calc() -> None:
    """
    A simple console calculator that performs basic arithmetic operations.

    Operations supported: addition (+), subtraction (-), multiplication (*), division (/).

    Handles exceptions:
        - ZeroDivisionError: Raised when dividing by zero.
        - ValueError: Raised when input is not a valid number.
        - UnknownOperationError: Raised when an invalid operation is entered.
        - OverflowError: Raised when a number is too large.
    """
    while True:
        try:
            num1 = float(input("Type the first number: "))
            operation = input("Type only (+, -, *, /) or 'exit' to terminate: ").strip().lower()

            if operation == 'exit':
                print("Terminating the program.")
                break

            num2 = float(input("Type the second number: "))

            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    raise ZeroDivisionError("Division by zero is not supported!")
                result = num1 / num2
            else:
                raise UnknownOperationError("Unknown operation! Type only +, -, *, or /.")

            print(f"Result: {result}")

        except ValueError:
            print("Error: Please enter a valid number.")
        except ZeroDivisionError as e:
            print(f"Error: {e}")
        except UnknownOperationError as e:
            print(f"Error: {e}")
        except OverflowError:
            print("Error: The number is too large!")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    simple_calc()
