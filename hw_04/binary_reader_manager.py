from typing import Iterator


class BinaryFileReader:
    """
    Context manager for reading binary files in large blocks.
    """

    def __init__(self, file_path: str, block_size: int = 1024) -> None:
        """
        Initializes the BinaryFileReader.

        Args:
            file_path (str): Path to the binary file.
            block_size (int): Number of bytes to read at a time. Defaults to 1024.
        """
        self.file_path: str = file_path
        self.block_size: int = block_size
        self.file = None

    def __enter__(self) -> "BinaryFileReader":
        """
        Opens the file in binary mode.

        Returns:
            BinaryFileReader: The context manager instance.
        """
        self.file = open(self.file_path, "rb")
        return self

    def read_blocks(self) -> Iterator[bytes]:
        """
        Reads the file in blocks.

        Yields:
            bytes: A block of file data.
        """
        total_bytes_read = 0
        while True:
            block = self.file.read(self.block_size)
            if not block:
                break
            total_bytes_read += len(block)
            print(f"Read {len(block)} bytes (Total: {total_bytes_read} bytes)")
            yield block

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Closes the file upon exiting the context.
        """
        if self.file:
            self.file.close()
        print("File closed.")


# Example usage
if __name__ == "__main__":
    file_path = "some.txt"  # Change to a valid binary file path

    with BinaryFileReader(file_path) as reader:
        for block in reader.read_blocks():
            pass  # Process block if needed
