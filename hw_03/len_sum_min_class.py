from typing import Generator, Any


class MyList:
    """
    A custom list implementation with additional functionality for length,
    summation, and finding the minimum value.
    """

    def __init__(self, *args: Any):
        """
        Initialize the custom list with given elements.

        Args:
            *args: Elements to include in the list.
        """
        self.items = list(args)

    def __len__(self) -> int:
        """
        Get the number of elements in the list.

        Returns:
            int: The length of the list.
        """
        return len(self.items)

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Allow iteration over the list elements.

        Yields:
            Any: Each element in the list.
        """
        for item in self.items:
            yield item

    def my_sum(self) -> Any:
        """
        Calculate the sum of elements in the list.

        Returns:
            Any: The sum of all elements in the list.
        """
        return sum(self)

    def my_min(self) -> Any:
        """
        Find the minimum element in the list using insertion sort.

        Returns:
            Any: The smallest element in the list.

        Raises:
            ValueError: If the list is empty.
        """
        if not self.items:
            raise ValueError("my_min() list of arguments is empty")

        items_copy = self.items[:]
        for i in range(1, len(items_copy)):
            current = items_copy[i]
            j = i - 1
            while j >= 0 and items_copy[j] > current:
                items_copy[j + 1] = items_copy[j]
                j -= 1
            items_copy[j + 1] = current

        # Minimum element is the first in the sorted list
        return items_copy[0]


def test_my_list():
    """
    Test the MyList class for length, sum, and minimum.
    """
    my_list = MyList(10, 20, 5, 30)

    print(f"Length of my_list: {len(my_list)}")  # Expected: 4

    print(f"Sum of my_list: {my_list.my_sum()}")  # Expected: 65

    print(f"Min of my_list: {my_list.my_min()}")  # Expected: 5


test_my_list()
