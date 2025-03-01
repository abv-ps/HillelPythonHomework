"""
This module defines classes for database models and a handler for performing database operations.

Classes:
- BaseModel: A base class for all database models, providing metadata for the table, columns,
  and primary key.
- Movie: Represents a movie entity with attributes such as title, release year, and genre.
- Actor: Represents an actor entity with attributes like name and birth year.
- MovieCast: Represents a relationship between a movie and an actor, linking the two through
  their respective IDs.
- DatabaseHandler: A generic class that provides methods for batch inserting records and
  retrieving entity IDs based on their identifier column.

Functions:
- insert(connection: sqlite3.Connection, data: list[T], model: Type[T]): Inserts multiple records
  into the database for a given model.
- get_id(connection: sqlite3.Connection, model: Type[T], identifier_value: Any): Retrieves the ID
  of an entity by searching its identifier column.
- find_by_keyword(connection: sqlite3.Connection, table: str, keyword: str, columns: Optional[list[str]] = None,
  order_by: Optional[str] = None) -> list[tuple]: Finds entries in a table matching a keyword.

This module is designed to simplify the process of working with a database that stores movies,
actors, and their relationships.
"""

import sqlite3
from typing import Optional, TypeVar, Generic, Type, Any, ClassVar
from dataclasses import dataclass

T = TypeVar("T", bound="BaseModel")


class BaseModel:
    """
    Base class for database models. Provides table metadata.
    """
    TABLE_NAME: ClassVar[str]
    COLUMNS: ClassVar[tuple[str, ...]]
    PRIMARY_KEY: ClassVar[Optional[str]]
    IDENTIFIER_COLUMN: ClassVar[Optional[str]]


@dataclass
class Movie(BaseModel):
    """
    Represents a movie entity.
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
    """

    @staticmethod
    def insert(connection: sqlite3.Connection, data: list[T], model: Type[T]) -> None:
        """
        Inserts multiple records into the database.

        Args:
            connection (sqlite3.Connection): The database connection.
            data (list[T]): A list of model instances to insert.
            model (Type[T]): The model class representing the table.
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
            connection (sqlite3.Connection): The database connection.
            model (Type[T]): The model class representing the table.
            identifier_value (Any): The value to search for in the identifier column.

        Returns:
            Optional[int]: The entity ID if found, otherwise None.
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
    def case_insensitive_collation(str1: str, str2: str) -> int:
        """
        A simple case-insensitive comparison function for SQLite.

        This function is intended to be used in SQLite queries to perform case-insensitive string comparisons.

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
                        columns: Optional[list[str]] = None, order_by: Optional[str] = None) -> list[tuple]:
        """
        Finds entries in a table matching a keyword.

        Args:
            connection (sqlite3.Connection): The database connection.
            table (str): The table name to search in.
            keyword (str): The keyword to search for.
            columns (Optional[list[str]]): The list of columns to return. Defaults to all columns.
            order_by (Optional[str]): An optional column to order the results by.

        Returns:
            list[tuple]: A list of matching rows from the database.
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
