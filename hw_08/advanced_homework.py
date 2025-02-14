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
- `AsyncFetcher` for asynchronous data fetching with event dispatching.

Usage examples are provided in docstrings for each class and function.
"""

import asyncio
from typing import Any, Awaitable, Callable, Generic, Dict, Type
from typing import Optional, Protocol, TypeVar, List, TypedDict
from abc import ABC, abstractmethod
from web_service_async import WebService

T = TypeVar("T")


class User(TypedDict):
    """
    Represents a user in the database.

    Attributes:
        id (int): User ID.
        name (str): Username.
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
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            Optional[User]: The user if found, else None.
        """

    def save_user(self, user: User) -> None:
        """
        Save a user to the database.

        Args:
            user (User): The user to be saved.

        Returns:
            None
        """


class InMemoryUserDB(UserDatabase):
    """
    In-memory user database implementation.

    This class provides an in-memory implementation of the UserDatabase protocol.
    It allows for storing users in a dictionary and retrieving them by their user ID.

    Attributes:
        users (Dict[int, User]): A dictionary where the keys are user IDs
                                    and the values are User objects.

    Methods:
        get_user(user_id: int) -> Optional[User]: Retrieves a user by their ID,
                                                    or None if not found.
        save_user(user: User) -> None: Saves a user to the in-memory database.
    """

    def __init__(self) -> None:
        """
        Initializes the in-memory user database.

        The users dictionary is initialized as an empty dictionary.
        """
        self.users: Dict[int, User] = {}

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID from the in-memory database.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, otherwise None.
        """
        return self.users.get(user_id)

    def save_user(self, user: User) -> None:
        """
        Saves a user to the in-memory database.

        Args:
            user (User): The user object to save.
        """
        self.users[user["id"]] = user


class Processor(Generic[T]):
    """
    A generic class for applying a function to each element in a list of data.

    This class provides a mechanism to process a list of data elements by applying
    a function to each element and returning a list of transformed results.

    Attributes:
        data (List[T]): A list of elements of type T that will be processed.

    Methods:
        apply(func: Callable[[T], T]) -> List[T]:
            Applies a function to each element of the data list and
            returns a list of transformed elements.
    """

    def __init__(self, data: List[T]) -> None:
        """
        Initializes the Processor with a list of data elements.

        Args:
            data (List[T]): A list of elements of type T that will be processed by the apply method.
        """
        self.data: List[T] = data

    def apply(self, func: Callable[[T], T]) -> List[T]:
        """
        Applies a transformation function to each element in the data list.

        Args:
            func (Callable[[T], T]): A function that takes an element of type T as input
                                      and returns a transformed element of the same type T.

        Returns:
            List[T]: A list of transformed elements, where each element is the result of applying
                      the function to the corresponding element from the original data list.
        """
        return [func(item) for item in self.data]


class FinalMeta(type):
    """
    Metaclass preventing subclassing.
    """

    def __new__(mcs: Type["FinalMeta"], name: str, bases: tuple[type], dct: dict) -> type:
        """
        Prevent subclassing of classes defined with this metaclass.

        Args:
            mcs (Type[FinalMeta]): The metaclass itself.
            name (str): The name of the class to be created.
            bases (type): The base classes of the class to be created.
            dct (dict): The dictionary containing class attributes.

        Raises:
            TypeError: If any base class has _is_final_class set to True.

        Returns:
            type: The new class.
        """
        for base in bases:
            if getattr(base, "_is_final_class", False):
                raise TypeError(f"Cannot subclass {name}, because {base.__name__} is final.")
        return super().__new__(mcs, name, bases, dct)


class Config(metaclass=FinalMeta):
    """
    Configuration class that cannot be subclassed.

    This class is designed to be a base for configuration settings that
    should not be extended or modified by subclasses.

    Example:
        >>> class SubConfig(Config):  # This should raise a TypeError
        ...     pass
        Traceback (most recent call last):
            ...
        TypeError: Cannot subclass SubConfig, because Config is final.
    """
    _is_final_class = True


class BaseRepository(ABC):
    """
    Abstract base class for repositories that handle saving data.
    This class serves as a base for implementing various types of repositories.
    """

    @abstractmethod
    def save(self, data: Dict[str, Any]) -> None:
        """
        Save data to the repository.

        This method must be implemented in subclasses to define the way data is persisted.

        Args:
            data (Dict[str, Any]): A dictionary containing the data to be saved.

        Returns:
            None

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """


class SQLRepository(BaseRepository):
    """
    SQL repository implementation that stores data in a SQL database.
    This class implements the `save` method for storing data in a SQL database.
    """

    def save(self, data: Dict[str, Any]) -> None:
        """
        Save data to the SQL database.

        This method simulates saving data to an SQL database by printing it.
        In a real implementation, it would connect to a database and perform the save operation.

        Args:
            data (Dict[str, Any]): A dictionary containing the data to be saved.

        Returns:
            None
        """
        print(f"Saved to SQL DB: {data}")


class EventDispatcher:
    """
    Event dispatcher for registering and handling events.

    This class allows for registering event handlers and dispatching events
    with associated data. Handlers are called when their respective event is triggered.
    """

    def __init__(self) -> None:
        """
        Initializes the event dispatcher.

        Sets up an empty dictionary to store events and their associated handlers.

        Returns:
            None
        """
        self.events: Dict[str, List[Callable[[Any], None]]] = {}

    def register_event(self, name: str, handler: Callable[[Any], None]) -> None:
        """
        Register an event handler for a specific event.

        The handler is a function that will be called when the event is triggered.

        Args:
            name (str): The name of the event to register the handler for.
            handler (Callable[[Any], None]): The function that handles the event
                                                when it is triggered.

        Returns:
            None
        """
        if name not in self.events:
            self.events[name] = []
        self.events[name].append(handler)

    def dispatch_event(self, name: str, data: Any) -> None:
        """
        Dispatch an event, triggering all handlers registered for that event.

        The handlers are called with the provided event data.

        Args:
            name (str): The name of the event to dispatch.
            data (Any): The data to pass to the event handlers.

        Returns:
            None
        """
        for handler in self.events.get(name, []):
            handler(data)


class AsyncFetcher:
    """
    Asynchronous data fetcher with event dispatching.

    This class fetches data asynchronously from a web service and triggers events
    when the data is successfully fetched.
    """

    def __init__(self, dispatcher: EventDispatcher, web_service: WebService) -> None:
        """
        Initializes the AsyncFetcher.

        Args:
            dispatcher (EventDispatcher): The event dispatcher instance.
            web_service (WebService): The web service client for fetching data.
        """
        self.dispatcher = dispatcher
        self.web_service = web_service

    def fetch(self, url: str) -> Awaitable[Dict[str, Any]]:
        """
        Fetch data asynchronously using a web service.

        This method returns an `Awaitable`, not a coroutine, by immediately scheduling
        `_fetch_data` as a background task and returning the `Task` object.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            Awaitable[Dict[str, Any]]: A task that resolves with the response data once fetched.
        """
        return asyncio.create_task(self._fetch_data(url))

    async def _fetch_data(self, url: str) -> Dict[str, Any]:
        """
        Internal method to fetch data asynchronously.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            Dict[str, Any]: The fetched data.
        """
        result = await self.web_service.fetch_data(url)
        self.dispatcher.dispatch_event("http_response", result)
        return result


def on_http_response(data: Dict[str, Any]) -> None:
    """Handles HTTP response event."""
    print(f"Response for {data['url']}: {data['data']['message']} ({data['timestamp']})")


async def main_async() -> None:
    """
    Main asynchronous function to test AsyncFetcher.

    This function demonstrates how to use the `AsyncFetcher` class to fetch
    data asynchronously and handle the response using an event dispatcher.
    """
    dispatcher = EventDispatcher()
    web_service = WebService()
    dispatcher.register_event("http_response", on_http_response)
    fetcher = AsyncFetcher(dispatcher, web_service)

    url = "https://some.com"

    # Fetch data asynchronously
    result = await fetcher.fetch(url)

    # Ensure expected keys exist in the response
    assert isinstance(result, dict)
    assert "url" in result
    assert "data" in result

    print(f"Result received: {result}")


def run_tests() -> None:
    """
    Run all module tests.
    """
    db = InMemoryUserDB()
    db.save_user({"id": 1, "name": "Alice", "is_admin": False})
    assert db.get_user(1) == {"id": 1, "name": "Alice", "is_admin": False}
    assert db.get_user(2) is None

    p = Processor([1, 2, 3])
    assert p.apply(lambda x: x * 2) == [2, 4, 6]

    repo = SQLRepository()
    repo.save({"name": "Product1", "price": 10.5})


def main() -> None:
    """
    Entry point for running tests and async execution.
    """
    run_tests()

    # Run the asynchronous main function
    asyncio.run(main_async())


if __name__ == "__main__":
    main()