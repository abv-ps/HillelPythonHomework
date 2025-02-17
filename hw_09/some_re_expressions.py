import re
from typing import List

def validate_numbers(n: int, numbers: List[str]) -> List[bool]:
    """
    Checks if each element in the given list is a properly formatted number.
    Prints the result for each number.
    """
    pattern = r'^[+-]?(0|[1-9]\d*)(\.\d+)?$'  # Updated regex to handle valid numbers
    results = [bool(re.fullmatch(pattern, num)) for num in numbers]

    print("\nNumber Validation Results:")
    for num, res in zip(numbers, results):
        print(f"{num}: {'Valid' if res else 'Invalid'}")

    return results

def is_valid_roman_numeral(roman: str) -> bool:
    """
    Checks if the provided string is a valid Roman numeral (1 to 3999).
    Prints the result for the Roman numeral validation.
    """
    pattern = r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    result = bool(re.fullmatch(pattern, roman))

    print("\nRoman Numeral Validation:")
    if result:
        print(f"{roman} is valid Roman numeral")
    else:
        print(f"{roman} is invalid Roman numeral")

    return result

def extract_hex_colors(n: int, inputs: List[str]) -> List[str]:
    """
    Extracts valid CSS hex color codes from the given list of input strings.
    Prints the extracted hex color codes.
    """
    pattern = r'#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b'
    results = []

    print("\nResult of Hex Color Code Extraction:")
    for input_str in inputs:
        matches = re.findall(pattern, input_str)
        if matches:
            results.extend(matches)

    if results:
        print("Extracted hex colors:")
        for color in results:
            print(color)
    else:
        print("No valid hex color codes found.")

    return results

def get_int_input(prompt: str) -> int:
    """Helper function to safely get an integer input."""
    while True:
        try:
            return int(input(prompt).strip())  # Try to convert input to integer
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_string_input(prompt: str) -> str:
    """Helper function to get a valid string input."""
    return input(prompt).strip()

def main():
    n = get_int_input("Enter a valid number of test cases: ")  # Ensure valid integer
    numbers = [get_string_input(f'Enter the {i+1} number: ') for i in range(n)]
    validate_numbers(n, numbers)

    roman = get_string_input("\nEnter a Roman numeral to validate: ")
    is_valid_roman_numeral(roman)

    n = get_int_input("\nEnter the number of test cases for hex color extraction: ")  # Ensure valid integer
    inputs = [get_string_input(f'Enter the {i+1} string: ') for i in range(n)]
    extract_hex_colors(n, inputs)

if __name__ == '__main__':
    main()
