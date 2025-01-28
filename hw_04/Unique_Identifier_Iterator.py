import uuid
from typing import Iterator


class UniqueIdentifierIterator:
    """
    Iterator for generating unique identifiers.
    """

    def __init__(self, count: int) -> None:
        """
        Initialize the iterator.

        Args:
            count (int): The number of unique identifiers to generate.

        Raises:
            ValueError: If count is negative.
        """
        if count < 0:
            raise ValueError("Count must be a non-negative integer.")
        self.count: int = count
        self.generated: int = 0

    def __iter__(self) -> Iterator[str]:
        """
        Return the iterator itself.

        Returns:
            Iterator[str]: The iterator instance.
        """
        return self

    def __next__(self) -> str:
        """
        Generate the next unique identifier.

        Returns:
            str: The next unique identifier.

        Raises:
            StopIteration: If all identifiers have been generated.
        """
        if self.generated >= self.count:
            raise StopIteration

        unique_id = str(uuid.uuid4())  # Generate a unique UUID
        self.generated += 1
        return unique_id


if __name__ == "__main__":
    unique_id_iterator = UniqueIdentifierIterator(count=5)

    for unique_id in unique_id_iterator:
        print(unique_id)
