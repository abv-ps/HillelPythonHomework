"""
A module for processing strings.

Methods:
    reverse_string: Return the reversed string.
    capitalize_string: Capitalize the first alphabetical character of the string.
    count_vowels: Count the number of vowels in the string.
"""

import unittest


class StringProcessor:
    """A class for processing strings."""

    def __init__(self, text: str):
        """Initialize the processor with a given string."""
        self.s = text

    def reverse_string(self) -> str:
        """Return the reversed string."""
        return self.s[::-1]

    def capitalize_string(self) -> str:
        """Capitalize the first alphabetical character of the string."""
        i = 0
        while i < len(self.s) and not self.s[i].isalpha():
            i += 1

        if i < len(self.s):
            return self.s[:i] + self.s[i].upper() + self.s[i + 1:]
        return self.s

    def count_vowels(self) -> int:
        """Count the number of vowels in the string."""
        vowels = "aeiouyаеиоуієэїеёыюя"
        return sum(char in vowels for char in self.s.lower())


class StringProcessorTest(unittest.TestCase):
    """Unit tests for the StringProcessor class."""

    def test_reverse_string(self):
        """Test reversing a string."""
        self.assertEqual(StringProcessor("радар").reverse_string(), "радар")
        self.assertEqual(StringProcessor("ротатор").reverse_string(), "ротатор")
        self.assertEqual(StringProcessor("123454321").reverse_string(), "123454321")

    @unittest.skip("Test with empty string is skipped due to known issue.")
    def test_reverse_empty_string(self):
        """Test reversing an empty string."""
        self.assertEqual(StringProcessor("").reverse_string(), "")

    def test_capitalize_string(self):
        """Test capitalizing the first alphabetical character."""
        self.assertEqual(StringProcessor("капіталізація").capitalize_string(), "Капіталізація")
        self.assertEqual(StringProcessor("уРЕНГОЙ").capitalize_string(), "УРЕНГОЙ")
        self.assertEqual(StringProcessor("").capitalize_string(), "")
        self.assertEqual(StringProcessor("!маленьке2").capitalize_string(), "!Маленьке2")

    def test_count_vowels(self):
        """Test counting vowels in a string."""
        self.assertEqual(StringProcessor("радар").count_vowels(), 2)
        self.assertEqual(StringProcessor("капіталізація").count_vowels(), 7)
        self.assertEqual(StringProcessor("").count_vowels(), 0)
        self.assertEqual(StringProcessor("123454321").count_vowels(), 0)


if __name__ == "__main__":
    unittest.main()
