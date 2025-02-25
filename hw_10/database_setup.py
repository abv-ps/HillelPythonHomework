"""
This module handles the setup and initialization of an SQLite database for storing movie data,
including movies, actors, and their relationships.

Functions:
- create_tables(cursor: sqlite3.Cursor): Creates the necessary tables in the database for storing
  movie, actor, and movie-actor relationship data.
- insert_movies(cursor: sqlite3.Cursor, movies: list[Movie]): Inserts a list of Movie objects
  into the database.
- insert_actors(cursor: sqlite3.Cursor, actors: list[Actor]): Inserts a list of Actor objects
  into the database.
- get_movie_id(cursor: sqlite3.Cursor, title: str): Retrieves the ID of a movie by its title from
  the database.
- get_actor_id(cursor: sqlite3.Cursor, name: str): Retrieves the ID of an actor by their name from
  the database.
- insert_movie_cast(cursor: sqlite3.Cursor, movie_cast: list[MovieCast]): Inserts a list of
  MovieCast objects into the database, establishing relationships between movies and actors.
- load_csv(filename: str): Loads data from a CSV file and returns it as a list of rows, excluding
  the header.

This module is designed to be run as a standalone script that will:
1. Initialize the Database class, which automatically connects to the SQLite database.
2. Create necessary tables if they do not already exist.
3. Load data from CSV files (movies, actors, and movie-actor relationships).
4. Insert the loaded data into the database.
5. Commit changes and close the connection to the database.
"""

import csv
import sqlite3
from typing import Optional, Callable, Any

from db_models import Actor, Movie, MovieCast, DatabaseHandler
from services import AutoEnsureCursorMeta


class Database(metaclass=AutoEnsureCursorMeta):
    """
    A class that manages the connection to an SQLite database and provides methods
    for creating tables, inserting data, and managing transactions.

    Attributes:
        db_path (str): Path to the SQLite database file.
        connection (sqlite3.Connection): SQLite connection object.
        cursor (sqlite3.Cursor): SQLite cursor object used for executing queries.

    Methods:
        __init__(): Establishes a connection to the SQLite database and initializes
            the cursor.
        __enter__(): Enables the use of this class in a context manager.
        __exit__(exc_type, exc_val, exc_tb): Commits changes and closes the connection
            after the context block. Rolls back the transaction if an exception occurs.
        create_tables(): Creates the necessary tables for movies, actors, and their relationships.
        insert_movies(movies: list[Movie]): Inserts a list of movies into the database.
        insert_actors(actors: list[Actor]): Inserts a list of actors into the database.
        insert_movie_cast(movie_cast: list[MovieCast]): Inserts movie-actor relationships
            into the database.
        get_movie_id(title: str): Retrieves a movie ID by its title.
        get_actor_id(name: str): Retrieves an actor ID by their name.
        start_savepoint(): Starts a savepoint to allow rollback or commit of changes.
        release_savepoint(): Releases the savepoint and commits changes made since the savepoint.
        rollback_savepoint(): Rolls back to the savepoint and discards changes made since it.

    Raises:
        sqlite3.Error: If an SQLite error occurs during any database operation.
        ValueError: If there is an issue with the cursor during database operations.
    """

    def __init__(self, db_path: str):
        """
        Initializes the database connection.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        try:
            self.connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            self.cursor: sqlite3.Cursor = self.connection.cursor()
            print("Database connected successfully.")
        except sqlite3.OperationalError as e:
            print(f"Operational error: {e}. Unable to connect to the database.")
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}. Check the database file or permissions.")
        except sqlite3.Error as e:
            print(f"Unexpected SQLite error: {e}")

    def __enter__(self):
        """Enables using the class in a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commits changes and closes the connection after the context block."""
        if self.connection:
            try:
                if exc_type is None:
                    self.connection.commit()
                    print("Changes committed successfully.")
                else:
                    self.connection.rollback()
                    print(f"Transaction rolled back due to: {exc_val}")
            except sqlite3.Error as e:
                print(f"Error committing/rolling back: {e}")
            finally:
                if self.cursor:
                    self.cursor.close()
                self.connection.close()
                print("Database connection closed.")

    def create_tables(self) -> None:
        """
        Creates tables for movies, actors, and their relationships if they do not exist.
        """
        try:
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            self.cursor.executescript('''
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    release_year INTEGER NOT NULL,
                    genre TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS actors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birth_year INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS movie_cast (
                    movie_id INTEGER,
                    actor_id INTEGER,
                    PRIMARY KEY (movie_id, actor_id),
                    FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
                    FOREIGN KEY (actor_id) REFERENCES actors (id) ON DELETE CASCADE
                );
            ''')
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def insert_movies(self, movies: list[Movie]) -> None:
        """Inserts a list of movies into the database."""
        DatabaseHandler.insert(self.connection, movies, Movie)

    def insert_actors(self, actors: list[Actor]) -> None:
        """Inserts a list of actors into the database."""
        DatabaseHandler.insert(self.connection, actors, Actor)

    def insert_movie_cast(self, movie_cast: list[MovieCast]) -> None:
        """Inserts movie-actor relationships into the database."""
        DatabaseHandler.insert(self.connection, movie_cast, MovieCast)

    def get_movie_id(self, title: str) -> Optional[int]:
        """Retrieves a movie ID by title."""
        return DatabaseHandler.get_id(self.connection, Movie, title)

    def get_actor_id(self, name: str) -> Optional[int]:
        """Retrieves an actor ID by name."""
        return DatabaseHandler.get_id(self.connection, Actor, name)

    def start_savepoint(self):
        """Starts a SAVEPOINT."""
        self.cursor.execute("SAVEPOINT temp_savepoint;")

    def release_savepoint(self):
        """Releases the SAVEPOINT (commits changes since the savepoint)."""
        self.cursor.execute("RELEASE SAVEPOINT temp_savepoint;")

    def rollback_savepoint(self):
        """Rolls back to the SAVEPOINT (discards changes since the savepoint)."""
        self.cursor.execute("ROLLBACK TO SAVEPOINT temp_savepoint;")

    def execute_query(self, query: str, params: tuple = (), column_index: int = 0) -> list:
        """
        Executes a query and returns a list of values from a specific column (default is column 0).

        Args:
            query (str): The SQL query to execute.
            params (tuple): Parameters to bind to the query.
            column_index (int): The index of the column to return values from (default is 0).

        Returns:
            list: A list of values from the specified column of the query result.
        """
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        return [row[column_index] for row in result]

    def register_custom_function(self, func_name: str,
                                 num_args: int,
                                 func: Callable[..., Any]
                                 ) -> None:
        """
        Registers a custom function with the SQLite connection.
        """
        self.connection.create_function(func_name, num_args, func)
        print(f"Custom function '{func_name}' registered.")

    def has_function(self, func_name: str) -> bool:
        """
        Checks if a custom function is already registered in SQLite.

        Args:
            func_name (str): The name of the function to check.

        Returns:
            bool: True if the function exists, False otherwise.
        """
        self.cursor.execute("PRAGMA function_list;")
        functions = [row[1] for row in self.cursor.fetchall()]
        return func_name in functions


def load_csv(filename: str) -> list[list[str]]:
    """
    Loads a CSV file and returns its content as a list of lists.

    Args:
        filename (str): The name of the CSV file.

    Returns:
        list[list[str]]: List of rows from the CSV file, excluding the header.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data[1:]


if __name__ == '__main__':
    with Database('kinodb.db') as db:
        print("Starting to create tables.")
        db.create_tables()

        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = db.cursor.fetchall()

        for table in tables:
            print(f"The table {table[0]} was created")

        movies_data = load_csv('movies.csv')
        actors_data = load_csv('actors.csv')

        movies_list = [Movie(row[0], int(row[1]), row[2]) for row in movies_data]
        actors_list = [Actor(row[1], int(row[2])) for row in actors_data]

        db.insert_movies(movies_list)
        db.insert_actors(actors_list)

        movie_cast_set = set()

        for m_title, a_name, _ in actors_data:
            movie_id = db.get_movie_id(m_title)
            actor_id = db.get_actor_id(a_name)
            if movie_id and actor_id:
                movie_cast_set.add((movie_id, actor_id))

        movie_cast_list = [MovieCast(movie_id, actor_id) for movie_id, actor_id in movie_cast_set]

        db.insert_movie_cast(movie_cast_list)

        print("Database setup completed successfully!")
