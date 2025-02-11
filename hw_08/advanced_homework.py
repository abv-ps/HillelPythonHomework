"""
This module provides various utilities and classes for working with users, data processing,
and event handling. It includes:

- A `User` TypedDict for user representation.
- `UserDatabase` protocol defining basic database operations.
- `InMemoryUserDB` implementation storing users in memory.
- `Processor` generic class for applying functions to data.
- `FinalMeta` metaclass preventing subclassing.
- `Config` class utilizing `FinalMeta`.
- `BaseRepository` and `SQLRepository` for data persistence.
- `EventDispatcher` for event handling.
- `AsyncFetcher` for asynchronous data fetching.

Usage examples are provided in docstrings for each class and function.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Awaitable, Optional, Protocol, TypeVar, Callable, Generic, List, TypedDict
from abc import ABC, abstractmethod
from web_service_async import WebService

T = TypeVar('T')


class User(TypedDict):
    """
    Represents a user in the database.

    Attributes:
        id (int): User ID.
        name (str): User name.
        is_admin (bool): Whether the user is an administrator.
    """
    id: int
    name: str
    is_admin: bool


class UserDatabase(Protocol):
    """
    Protocol for user database operations.
    """

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        pass

    def save_user(self, user: User) -> None:
        """Save a user to the database."""
        pass


class InMemoryUserDB(UserDatabase):
    """
    In-memory user database implementation.
    """

    def __init__(self) -> None:
        self.users: Dict[int, User] = {}

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def save_user(self, user: User) -> None:
        self.users[user['id']] = user


class Processor(Generic[T]):
    """
    A generic class for applying functions to a list of data elements.
    """

    def __init__(self, data: List[T]) -> None:
        self.data = data

    def apply(self, func: Callable[[T], T]) -> List[T]:
        return [func(item) for item in self.data]


class FinalMeta(type):
    """
    Metaclass preventing subclassing.
    """

    def __new__(cls, name, bases, dct):
        for base in bases:
            if getattr(base, "_is_final_class", False):
                raise TypeError(f"Cannot subclass {name}, because {base.__name__} is final.")
        return super().__new__(cls, name, bases, dct)


class Config(metaclass=FinalMeta):
    """
    Configuration class that cannot be subclassed.

    Example:
        >>> class SubConfig(Config)  # This should raise a TypeError
        ...     pass
        Traceback (most recent call last):
            ...
        TypeError: Cannot subclass SubConfig, because Config is final.
    """
    _is_final_class = True


class BaseRepository(ABC):
    """
    Abstract base class for repositories.
    """

    @abstractmethod
    def save(self, data: Dict[str, Any]) -> None:
        pass


class SQLRepository(BaseRepository):
    """
    SQL repository implementation.
    """

    def save(self, data: Dict[str, Any]) -> None:
        print(f"Saved to SQL DB: {data}")


class EventDispatcher:
    """
    Event dispatcher for registering and handling events.
    """

    def __init__(self) -> None:
        self.events: Dict[str, List[Callable[[Any], None]]] = {}

    def register_event(self, name: str, handler: Callable[[Any], None]) -> None:
        if name not in self.events:
            self.events[name] = []
        self.events[name].append(handler)

    def dispatch_event(self, name: str, data: Any) -> None:
        for handler in self.events.get(name, []):
            handler(data)


class AsyncFetcher:
    """
    Asynchronous data fetcher with event dispatching.
    """

    def __init__(self, dispatcher: EventDispatcher, web_service: WebService) -> None:
        self.dispatcher = dispatcher
        self.web_service = web_service

    async def fetch(self, url: str) -> Awaitable[Dict[str, Any]]:
        """
        Fetch data asynchronously using a web service.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            Awaitable[Dict[str, Any]]: The result, which will contain the data or an error message.
        """
        loop = asyncio.get_running_loop()
        future: asyncio.Future[Dict[str, Any]] = loop.create_future()

        async def _fetch():
            result = await self.web_service.fetch_data(url)
            self.dispatcher.dispatch_event("http_response", result)
            future.set_result(result)

        loop.create_task(_fetch())
        return future


def on_http_response(data: Dict[str, Any]) -> None:
    """Handles HTTP response event."""
    print(f"Response for {data['url']}: {data['data']['message']} ({data['timestamp']})")


async def main_async() -> None:
    dispatcher = EventDispatcher()
    web_service = WebService()
    dispatcher.register_event("http_response", on_http_response)
    fetcher = AsyncFetcher(dispatcher, web_service)  # Додаємо `web_service`

    url = "https://example.com"  # Визначаємо URL перед використанням
    result = await fetcher.fetch(url)

    print(f"Результат отримано: {result}")

def run_tests() -> None:
    """Run all module tests."""
    db = InMemoryUserDB()
    db.save_user({"id": 1, "name": "Alice", "is_admin": False})
    assert db.get_user(1) == {"id": 1, "name": "Alice", "is_admin": False}
    assert db.get_user(2) is None

    p = Processor([1, 2, 3])
    assert p.apply(lambda x: x * 2) == [2, 4, 6]

    repo = SQLRepository()
    repo.save({"name": "Product1", "price": 10.5})


def main() -> None:
    """Entry point for running tests and async execution."""
    run_tests()
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
