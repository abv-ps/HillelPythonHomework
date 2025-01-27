from typing import Iterator, Optional


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
        self.current_position: Optional[int] = None
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
        if self.current_position is None:
            self._initialize_positions()

        if self.lines_read >= self.n:
            raise StopIteration

        line = self._get_next_line()
        if line is not None:
            self.lines_read += 1
            return line
        else:
            raise StopIteration

    def _initialize_positions(self) -> None:
        """
        Initializes the current position for reading the file.
        """
        with open(self.file_name, 'r', encoding=self.encoding, errors='replace') as file:
            file.seek(0, 2)  # Move to the end of the file
            self.current_position = file.tell()  # Start reading from the end of the file

    def _get_next_line(self) -> Optional[str]:
        """
        Retrieves the next line in reverse order.

        Returns:
            Optional[str]: The next line if available, otherwise None.
        """
        with open(self.file_name, 'r', encoding=self.encoding, errors='replace') as file:
            line = ''
            file.seek(self.current_position)

            while self.current_position > 0:
                self.current_position -= 1
                file.seek(self.current_position)
                char = file.read(1)

                if char == '\n' and line:  # End of a line
                    return line.strip()

                line = char + line

            # Return the first line if we reach the beginning
            if self.current_position == 0 and line:
                return line.strip()

        return None


# Використання ітератора
file_iterator = ReversedNStringFileIterator("some.txt", n=10)

for line in file_iterator:
    print(line)
