from typing import List


class Person:
    """
    A class to represent a person with a name and age.

    Args:
        name (str): The name of the person.
        age (int): The age of the person.
    """

    def __init__(self, name: str, age: int):
        """
        Initialize a person with a name and age.

        Args:
            name (str): The name of the person.
            age (int): The age of the person.
        """
        self.name = name
        self.age = age

    def __lt__(self, other: "Person") -> bool:
        """
        Check if the current person's age is less than the other person's age.

        Args:
            other (Person): The person to compare to.

        Returns:
            bool: True if the current person's age is less, False otherwise.
        """
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age

    def __eq__(self, other: "Person") -> bool:
        """
        Check if the current person's age is equal to the other person's age.

        Args:
            other (Person): The person to compare to.

        Returns:
            bool: True if both persons have the same age, False otherwise.
        """
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age

    def __gt__(self, other: "Person") -> bool:
        """
        Check if the current person's age is greater than the other person's age.

        Args:
            other (Person): The person to compare to.

        Returns:
            bool: True if the current person's age is greater, False otherwise.
        """
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age

    def __repr__(self) -> str:
        """
        Return a string representation of the person.

        Returns:
            str: A string in the format 'name, age years old'.
        """
        return f"{self.name}, {self.age} years old"


def sort_people(people: List[Person]) -> List[Person]:
    """
    Sort a list of Person objects by age using insertion sort.

    Args:
        people (List[Person]): A list of Person objects to be sorted.

    Returns:
        List[Person]: The sorted list of Person objects.
    """
    for i in range(1, len(people)):
        current_person = people[i]
        j = i - 1
        # Move all elements greater than the current person to one position up
        while j >= 0 and people[j] > current_person:
            people[j + 1] = people[j]
            j -= 1
        # Insert the current person at the correct position
        people[j + 1] = current_person
    return people


people = [
    Person("Ivan", 18),
    Person("Anna", 33),
    Person("Zina", 24)
]

sorted_people = sort_people(people)

for person in sorted_people:
    print(person)
