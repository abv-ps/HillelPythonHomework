"""
This module defines classes for database models and a handler for performing common
database operations.

Classes:
    - BaseModel: A base class for all database models, providing metadata for table names, columns,
      and primary keys.
    - Movie: Represents a movie entity, including attributes like title, release year, and genre.
    - Actor: Represents an actor entity, including attributes like name and birth year.
    - MovieCast: Represents the relationship between a movie and an actor,
      linking them through their respective IDs.
    - DatabaseHandler: A generic class that provides methods for batch inserting records and
      retrieving entity IDs based on their identifier column.

Functions:
    - insert(connection: sqlite3.Connection, data: list[T], model: Type[T]) -> None:
        Inserts multiple records into the database for the given model.
    - get_id(connection: sqlite3.Connection, model: Type[T],
             identifier_value: Any) -> Optional[int]:
        Retrieves the ID of an entity by searching for its identifier column.
    - find_by_keyword(connection: sqlite3.Connection, table: str, keyword: str,
                      columns: Optional[list[str]] = None,
                      order_by: Optional[str] = None) -> list[tuple]:
        Finds entries in a table that match the given keyword.

This module simplifies the process of working with a database that stores information about movies,
actors, and their relationships, providing a clean and efficient way to interact with the data.
"""

import sqlite3
from typing import Optional, TypeVar, Generic, Type, Any, ClassVar
from dataclasses import dataclass

T = TypeVar("T", bound="BaseModel")


class BaseModel:
    """
    Base class for database models. Provides table metadata and ensures that
    all models have necessary attributes, such as table name, columns, and primary key.

    Attributes:
        TABLE_NAME (ClassVar[str]): Name of the table in the database.
        COLUMNS (ClassVar[tuple[str, ...]]): Tuple of column names for the model's table.
        PRIMARY_KEY (ClassVar[Optional[str]]): The primary key column name for the table,
        or None if not applicable.
        IDENTIFIER_COLUMN (ClassVar[Optional[str]]): The column name used to uniquely identify
        rows in the table.
    """

    TABLE_NAME: ClassVar[str]
    COLUMNS: ClassVar[tuple[str, ...]]
    PRIMARY_KEY: ClassVar[Optional[str]]
    IDENTIFIER_COLUMN: ClassVar[Optional[str]]


@dataclass
class Movie(BaseModel):
    """
    Represents a movie entity.

    Attributes:
        title (str): The title of the movie.
        release_year (int): The year the movie was released.
        genre (Optional[str]): The genre of the movie. Can be None if not specified.
    """
    title: str
    release_year: int
    genre: Optional[str]

    TABLE_NAME = "movies"
    COLUMNS = ("title", "release_year", "genre")
    PRIMARY_KEY = "id"
    IDENTIFIER_COLUMN = "title"


@dataclass
class Actor(BaseModel):
    """
    Represents an actor entity.

    Attributes:
        name (str): The name of the actor.
        birth_year (int): The birth year of the actor.

    Class Variables:
        TABLE_NAME (ClassVar[str]): The name of the table in the database.
        COLUMNS (ClassVar[tuple[str, ...]]): Tuple of column names for the model's table.
        PRIMARY_KEY (ClassVar[Optional[str]]): The primary key column name for the table.
        IDENTIFIER_COLUMN (ClassVar[Optional[str]]): The column name used to uniquely identify
        rows in the table.
    """
    name: str
    birth_year: int

    TABLE_NAME = "actors"
    COLUMNS = ("name", "birth_year")
    PRIMARY_KEY = "id"
    IDENTIFIER_COLUMN = "name"


@dataclass
class MovieCast(BaseModel):
    """
    Represents a relationship between a movie and an actor.

    This class models the many-to-many relationship between movies and actors in the database.
    Each instance of this class represents a row in the `movie_cast` table, which links an actor
    to a movie via their respective IDs.

    Attributes:
        movie_id (int): The ID of the movie.
        actor_id (int): The ID of the actor.

    Class Variables:
        TABLE_NAME (ClassVar[str]): The name of the table in the database.
        COLUMNS (ClassVar[tuple[str, ...]]): Tuple of column names for the model's table.
        PRIMARY_KEY (ClassVar[Optional[str]]): No primary key defined for this table.
        IDENTIFIER_COLUMN (ClassVar[Optional[str]]): No identifier column defined for this table.
    """
    movie_id: int
    actor_id: int

    TABLE_NAME = "movie_cast"
    COLUMNS = ("movie_id", "actor_id")
    PRIMARY_KEY = None  # No primary key defined
    IDENTIFIER_COLUMN = None


class DatabaseHandler(Generic[T]):
    """
    Handles batch insert operations and entity lookups for different database models.

    This generic class provides utility methods for performing batch insert operations
    and retrieving  entity IDs by their identifier column for any model that inherits
    from `BaseModel`.

    Methods:
        insert(connection: sqlite3.Connection, data: list[T], model: Type[T]) -> None:
            Inserts multiple records into the database for a given model.

        get_id(connection: sqlite3.Connection, model: Type[T],
               identifier_value: Any) -> Optional[int]:
            Retrieves the ID of an entity by searching for its identifier column value.

        case_insensitive_collation(str1: str, str2: str) -> int:
            Compares two strings in a case-insensitive manner, intended for SQLite queries.

        find_by_keyword(connection: sqlite3.Connection, table: str, keyword: str,
                        columns: Optional[list[str]] = None,
                        order_by: Optional[str] = None) -> list[tuple]:
            Finds entries in a table matching a keyword.

    Type Parameters:
        T: A type variable bound to `BaseModel`, representing the model type that is being handled.
    """

    @staticmethod
    def insert(connection: sqlite3.Connection, data: list[T], model: Type[T]) -> None:
        """
        Inserts multiple records into the database for a given model.

        Args:
            connection (sqlite3.Connection): The active SQLite database connection.
            data (list[T]): A list of model instances (e.g., `Movie`, `Actor`, etc.)
            to be inserted into the database.
            model (Type[T]): The model class representing the database table
            (e.g., `Movie` or `Actor`).

        Raises:
            sqlite3.Error: If an error occurs during the insert operation.
        """
        if not data:
            return

        cursor = connection.cursor()
        table_name = model.TABLE_NAME
        columns = model.COLUMNS
        placeholders = ", ".join("?" for _ in columns)
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        values = [tuple(getattr(item, col) for col in columns) for item in data]
        cursor.executemany(query, values)

    @staticmethod
    def get_id(connection: sqlite3.Connection, model: Type[T],
               identifier_value: Any) -> Optional[int]:
        """
        Retrieves the entity ID by its identifier column.

        Args:
            connection (sqlite3.Connection): The active database connection.
            model (Type[T]): The model class representing the table (e.g., `Movie`, `Actor`).
            identifier_value (Any): The value to search for in the identifier column.

        Returns:
            Optional[int]: The entity ID if found, otherwise None.

        Raises:
            ValueError: If the model does not have an identifier column defined.
            sqlite3.Error: If an error occurs while executing the query.
        """
        cursor = connection.cursor()
        table_name = model.TABLE_NAME
        primary_key = model.PRIMARY_KEY
        identifier_column = model.IDENTIFIER_COLUMN

        if not identifier_column:
            raise ValueError(f"Model {model.__name__} does not have an identifier column.")

        query = f"SELECT {primary_key} FROM {table_name} WHERE {identifier_column} = ?"
        cursor.execute(query, (identifier_value,))
        result = cursor.fetchone()
        return result[0] if result else None

    @staticmethod
    def get_name_by_id(connection: sqlite3.Connection, model_name: str, item_id: int) -> Optional[str]:
        """
        Retrieves the name or title of an item (actor or movie) by its ID.

        Args:
            connection (sqlite3.Connection): The active database connection.
            model_name (str): The name of the model class (e.g., 'Actor' or 'Movie').
            item_id (int): The ID of the item (actor or movie) to search for.

        Returns:
            Optional[str]: The name or title of the item if found, otherwise None.
        """
        model_name = model_name.capitalize()

        model = globals().get(model_name)

        if not model:
            raise ValueError(f"Model {model_name} not found.")

        cursor = connection.cursor()

        # Отримуємо дані з моделі
        table_name = model.TABLE_NAME
        identifier_column = model.IDENTIFIER_COLUMN

        query = f"SELECT {identifier_column} FROM {table_name} WHERE id = ?"
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()

        return result[0] if result else None

    @staticmethod
    def case_insensitive_collation(str1: str, str2: str) -> int:
        """
        A simple case-insensitive comparison function for SQLite.

        This function is intended to be used in SQLite queries to perform
        case-insensitive string comparisons.

        Args:
            str1 (str): The first string to compare.
            str2 (str): The second string to compare.

        Returns:
            int: A negative integer if str1 < str2, zero if str1 == str2,
                 or a positive integer if str1 > str2.
        """
        return (str1.lower() > str2.lower()) - (str1.lower() < str2.lower())

    @staticmethod
    def find_by_keyword(connection: sqlite3.Connection, table: str, keyword: str,
                        columns: Optional[list[str]] = None,
                        order_by: Optional[str] = None) -> list[tuple]:
        """
        Finds entries in a table matching a keyword.

        Args:
            connection (sqlite3.Connection): The active database connection.
            table (str): The name of the table in which to search.
            keyword (str): The keyword to search for in the specified table.
            columns (Optional[list[str]]): A list of column names to return,
                                           defaults to `["*"]` to return all columns.
            order_by (Optional[str]): The column name to order results by,
                                      or None if no ordering is desired.

        Returns:
            list[tuple]: A list of matching rows, each represented as a tuple of column values.

        Raises:
            sqlite3.Error: If an error occurs while querying the database.
        """
        cursor = connection.cursor()
        connection.create_collation("CI", DatabaseHandler.case_insensitive_collation)

        if not columns:
            columns = ["*"]

        query = f"SELECT {', '.join(columns)} FROM {table} WHERE {columns[0]} LIKE ? COLLATE CI"
        if order_by:
            query += f" ORDER BY {order_by}"

        cursor.execute(query, (f"%{keyword}%",))
        return cursor.fetchall() or []
