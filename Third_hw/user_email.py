import re


class User:
    def __init__(self, first_name: str, last_name: str, email: str):
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

        if not self._is_valid_email(email):
            raise ValueError(f"Invalid email format: {email}")

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value:
            raise ValueError("First name cannot be empty.")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value:
            raise ValueError("Last name cannot be empty.")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value: str):
        if not self._is_valid_email(value):
            raise ValueError(f"Invalid email format: {value}")
        self._email = value

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        email_regex = r'^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def __repr__(self):
        return f"User(first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}')"
