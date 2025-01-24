class BinaryNumber:
    """
    A class to represent a binary number and perform bitwise operations.

    Args:
        value (str): The binary number represented as a string of '0' and '1'.
    """

    def __init__(self, value: str):
        """
        Initialize a binary number.

        Args:
            value (str): A string representing a binary number.

        Raises:
            ValueError: If the provided value contains characters other than '0' or '1'.
        """
        if not all(c in '01' for c in value):
            raise ValueError("The value must be a binary number (only '0' and '1').")
        self.value = value

    def __and__(self, other: "BinaryNumber") -> "BinaryNumber":
        """
        Perform bitwise AND operation between two binary numbers.

        Args:
            other (BinaryNumber): Another BinaryNumber object.

        Returns:
            BinaryNumber: A new BinaryNumber object as the result.
        """
        max_len = max(len(self.value), len(other.value))
        self_padded = self.value.zfill(max_len)
        other_padded = other.value.zfill(max_len)
        result = ''.join('1' if self_padded[i] == '1' and other_padded[i] == '1' else '0' for i in range(max_len))
        return BinaryNumber(result)

    def __or__(self, other: "BinaryNumber") -> "BinaryNumber":
        """
        Perform bitwise OR operation between two binary numbers.

        Args:
            other (BinaryNumber): Another BinaryNumber object.

        Returns:
            BinaryNumber: A new BinaryNumber object as the result.
        """
        max_len = max(len(self.value), len(other.value))
        self_padded = self.value.zfill(max_len)
        other_padded = other.value.zfill(max_len)
        result = ''.join('1' if self_padded[i] == '1' or other_padded[i] == '1' else '0' for i in range(max_len))
        return BinaryNumber(result)

    def __xor__(self, other: "BinaryNumber") -> "BinaryNumber":
        """
        Perform bitwise XOR operation between two binary numbers.

        Args:
            other (BinaryNumber): Another BinaryNumber object.

        Returns:
            BinaryNumber: A new BinaryNumber object as the result.
        """
        max_len = max(len(self.value), len(other.value))
        self_padded = self.value.zfill(max_len)
        other_padded = other.value.zfill(max_len)
        result = ''.join('1' if self_padded[i] != other_padded[i] else '0' for i in range(max_len))
        return BinaryNumber(result)

    def __invert__(self) -> "BinaryNumber":
        """
        Perform bitwise NOT operation on the binary number.

        Returns:
            BinaryNumber: A new BinaryNumber object as the result.
        """
        result = ''.join('1' if bit == '0' else '0' for bit in self.value)
        return BinaryNumber(result)


def test_binary_operations():
    """
    Test the BinaryNumber class and its bitwise operations.
    """
    bin1 = BinaryNumber('1101')
    bin2 = BinaryNumber('1011')

    and_result = bin1 & bin2
    print(f"{bin1} & {bin2} = {and_result}")

    or_result = bin1 | bin2
    print(f"{bin1} | {bin2} = {or_result}")

    xor_result = bin1 ^ bin2
    print(f"{bin1} ^ {bin2} = {xor_result}")

    not_result = ~bin1
    print(f"~{bin1} = {not_result}")


test_binary_operations()
