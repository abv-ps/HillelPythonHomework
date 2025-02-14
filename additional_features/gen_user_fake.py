from faker import Faker
from typing import List, Dict


def generate_users(count: int = 15) -> List[Dict[str, str]]:
    """
    Generate a list of users with Ukrainian localization.

    Args:
        count (int): The number of users to generate. Default is 15.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing user data (name, surname, email).
    """
    fake = Faker('uk_UA')
    users = []
    for _ in range(count):
        user = {
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "email": fake.email()
        }
        users.append(user)
    return users


def main() -> None:
    """Generate and print user data."""
    users = generate_users()
    for user in users:
        print(user)


if __name__ == "__main__":
    main()
