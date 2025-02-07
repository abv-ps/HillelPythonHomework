"""
File Processing Module

This module provides functionality for reading and writing text files,
including handling large data volumes and filtering content based on specific conditions.

Features:
- `FileProcessor` class for basic file operations:
  - Writing data to a file.
  - Reading data from a file.
- Exception handling for missing files.
- Unit tests using `pytest`:
  - Temporary file creation using `tmpdir` fixture.
  - Tests for handling large data volumes and empty strings.
  - Exception handling tests for non-existent files.

Usage:
This module can be used for various file processing tasks,
including storing and retrieving text data efficiently.
"""
import os


class FileProcessor:
    """
    A utility class for file operations including reading and writing text data.
    """

    @staticmethod
    def write_to_file(file_path: str, data: str) -> None:
        """
        Writes the given data to a file.

        Args:
            file_path (str): The path to the file.
            data (str): The content to write into the file.
        """
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)

    @staticmethod
    def read_from_file(file_path: str) -> str:
        """
        Reads content from a file.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The content of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' not found.")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


# Tests using pytest
import pytest


def test_file_write_read(tmpdir) -> None:
    """
    Tests writing to and reading from a file.
    """
    file = tmpdir.join("testfile.txt")
    FileProcessor.write_to_file(str(file), "Hello, World!")
    content = FileProcessor.read_from_file(str(file))
    assert content == "Hello, World!"


def test_large_data_write_read(tmpdir) -> None:
    """
    Tests writing and reading large amounts of data.
    """
    file = tmpdir.join("largefile.txt")
    large_data = "A" * 10**6  # 1 million characters
    FileProcessor.write_to_file(str(file), large_data)
    content = FileProcessor.read_from_file(str(file))
    assert content == large_data


def test_empty_string_write_read(tmpdir) -> None:
    """
    Tests writing and reading an empty string.
    """
    file = tmpdir.join("emptyfile.txt")
    FileProcessor.write_to_file(str(file), "")
    content = FileProcessor.read_from_file(str(file))
    assert content == ""


def test_file_not_found() -> None:
    """
    Tests exception handling when trying to read a non-existent file.
    """
    with pytest.raises(FileNotFoundError):
        FileProcessor.read_from_file("non_existent_file.txt")
