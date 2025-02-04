from hw_06.my_package import factorial, gcd, to_uppercase, strip_spaces


def main():
    print("Mathematics operations:")

    # Calculating factorial
    values = [-1, 1, 0, 7]

    for value in values:
        try:
            print(f"Factorial of {value}: {factorial(value)}")
        except ValueError as e:
            print(f"Error calculating factorial of {value}: {e}")

    print(f"GCD of 33 and 57: {gcd(33, 57)}")

    print("\n" + ("_&_" * 27))

    print("\nOperations with strings:")

    # Converting to uppercase
    text = "you have to do better"
    print(f"Uppercase: {to_uppercase(text.split()[0][0])}{text.split()[0][1:]} "
          f"{' '.join(text.split()[1:-1])} {to_uppercase(text.split()[-1])}")

    # Stripping spaces
    text_with_spaces = "   you have to do better   "
    print(
        f"Stripped: '{strip_spaces(
            to_uppercase(text_with_spaces.split()[0][0]) + text_with_spaces.split()[0][1:]
            + ' ' +
            ' '.join(text_with_spaces.split()[1:-1])
            + ' ' +
            to_uppercase(text_with_spaces.split()[-1])
        )}'"
    )


if __name__ == "__main__":
    main()
