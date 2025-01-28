from typing import Iterator, Optional
from collections import deque

class ReversedNStringFileIterator:
    """
    Iterator for reading the last N lines of a file in reverse order.
    """

    def __init__(self, file_name: str, n: int = 10, encoding: str = 'utf-8') -> None:
        """
        Initializes the iterator.

        Args:
            file_name (str): The path to the file.
            n (int): The number of lines to read. Defaults to 10.
            encoding (str): The file encoding. Defaults to 'utf-8'.
        """
        self.file_name: str = file_name
        self.n: int = n
        self.encoding: str = encoding
        self.buffer: deque[str] = deque(maxlen=n)  # буфер для зберігання останніх N рядків
        self.lines_read: int = 0

    def __iter__(self) -> Iterator[str]:
        """
        Returns the iterator object.

        Returns:
            Iterator[str]: The iterator itself.
        """
        return self

    def __next__(self) -> str:
        """
        Reads the next line in reverse order.

        Returns:
            str: The next line from the file.

        Raises:
            StopIteration: If there are no more lines to read.
        """
        if not self.buffer:
            self._read_lines()

        if self.lines_read >= self.n or not self.buffer:
            raise StopIteration

        self.lines_read += 1
        return self.buffer.pop()

    def _read_lines(self) -> None:
        """
        Reads lines from the file and adds them to the buffer in reverse order.
        """
        with open(self.file_name, 'r', encoding=self.encoding, errors='replace') as file:
            # Читання файлу по рядках
            for line in file:
                self.buffer.append(line.strip())  # додаємо рядок до буфера

# Example usage
file_iterator = ReversedNStringFileIterator("some2.txt", n=10)

for line in file_iterator:
    print(line)
