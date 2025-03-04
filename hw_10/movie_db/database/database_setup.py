"""
This module handles the setup and initialization of an SQLite database for storing movie data,
including movies, actors, and their relationships.

Functions:
- create_tables(cursor: sqlite3.Cursor) -> None: Creates the necessary tables in the database
  for storing movie, actor, and movie-actor relationship data.
- insert_movies(cursor: sqlite3.Cursor, movies: list[Movie]) -> None: Inserts a list
  of Movie objects into the database.
- insert_actors(cursor: sqlite3.Cursor, actors: list[Actor]) -> None: Inserts a list
  of Actor objects into the database.
- get_movie_id(cursor: sqlite3.Cursor, title: str) -> Optional[int]: Retrieves the ID
  of a movie by its title from the database.
- get_actor_id(cursor: sqlite3.Cursor, name: str) -> Optional[int]: Retrieves the ID
  of an actor by their name from the database.
- insert_movie_cast(cursor: sqlite3.Cursor, movie_cast: list[MovieCast]) -> None: Inserts a list
  of MovieCast objects into the database, establishing relationships between movies and actors.
- load_csv(filename: str) -> list[list[str]]: Loads data from a CSV file and returns it as a list
  of rows, excluding the header.

This module is designed to be run as a standalone script that will:
1. Initialize the database class, which automatically connects to the SQLite database.
2. Create necessary tables if they do not already exist.
3. Load data from CSV files (movies, actors, and movie-actor relationships).
4. Insert the loaded data into the database.
5. Commit changes and close the connection to the database.

Usage:
    python -m movie_db.database.database_setup
    You should run this code at one level higher than the movie_db folder.
"""
import os
import sqlite3
from typing import Optional, Callable, Any

from .db_models import Actor, Movie, MovieCast, DatabaseHandler
from ..services.services import AutoEnsureCursorMeta
from ..utils.helpers import load_csv


class Database(metaclass=AutoEnsureCursorMeta):
    """
    A class that manages the connection to an SQLite database and provides methods
    for creating tables, inserting data, and managing transactions.

    This class provides a context manager for handling database connections and transactions,
    as well as methods for interacting with the database, including creating tables, inserting data,
    executing queries, and using savepoints for transaction management. It also allows
    the registration of custom functions for use within SQL queries.

    Attributes:
        db_path (str): Path to the SQLite database file.
        connection (sqlite3.Connection): SQLite database connection object.
        cursor (sqlite3.Cursor): SQLite cursor object for executing queries.

    Methods:
        __init__(): Establishes a connection to the SQLite database and initializes
            the cursor.
        __enter__: Prepares the database connection for use in a context manager.
        __exit__: Commits changes or rolls back transactions and closes the database connection.
        create_tables: Creates tables for movies, actors, and their relationships
        if they do not exist.
        insert_movies: Inserts a list of `Movie` objects into the database.
        insert_actors: Inserts a list of `Actor` objects into the database.
        insert_movie_cast: Inserts movie-actor relationships into the database.
        get_movie_id: Retrieves the movie ID by the movie title.
        get_actor_id: Retrieves the actor ID by the actor's name.
        start_savepoint: Starts a savepoint for transaction management.
        release_savepoint: Releases a savepoint, committing all changes made since the savepoint.
        rollback_savepoint: Rolls back the database to the state of the last savepoint.
        execute_query: Executes a SQL query with parameters and returns the results.
        register_custom_function: Registers a custom function for use in SQL queries.

    Raises:
        sqlite3.Error: If an SQLite error occurs during any database operation.
        ValueError: If there is an issue with the cursor during database operations.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initializes the database connection.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        try:
            self.connection: sqlite3.Connection = sqlite3.connect(self.db_path)
            self.cursor: sqlite3.Cursor = self.connection.cursor()
            print("database connected successfully.")
        except sqlite3.OperationalError as e:
            print(f"Operational error: {e}. Unable to connect to the database.")
        except sqlite3.DatabaseError as e:
            print(f"database error: {e}. Check the database file or permissions.")
        except sqlite3.Error as e:
            print(f"Unexpected SQLite error: {e}")

    def __enter__(self) -> 'Database':
        """Enables using the class in a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Commits changes and closes the connection after the context block."""
        if self.connection:
            try:
                if exc_type is None or SystemExit:
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

        This method checks for the existence of tables in the database and creates them
        if they are missing.
        The tables include:
        - `movies`: Stores movie details such as title, release year, and genre.
        - `actors`: Stores actor details like name and birth year.
        - `movie_cast`: Stores relationships between movies and actors, including foreign key constraints.

        Raises:
            sqlite3.Error: If an error occurs while creating the tables.
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
        """Inserts a list of movie-actor relationships into the database."""
        DatabaseHandler.insert(self.connection, movie_cast, MovieCast)

    def get_movie_id(self, title: str) -> Optional[int]:
        """Retrieves the movie ID by its title."""
        return DatabaseHandler.get_id(self.connection, Movie, title)

    def get_actor_id(self, name: str) -> Optional[int]:
        """Retrieves the actor ID by their name."""
        return DatabaseHandler.get_id(self.connection, Actor, name)

    def start_savepoint(self) -> None:
        """Starts a savepoint for transaction management."""
        self.cursor.execute("SAVEPOINT temp_savepoint;")

    def release_savepoint(self) -> None:
        """Releases the SAVEPOINT (commits changes since the savepoint)."""
        self.cursor.execute("RELEASE SAVEPOINT temp_savepoint;")

    def rollback_savepoint(self) -> None:
        """Rolls back to the SAVEPOINT (discards changes since the savepoint)."""
        self.cursor.execute("ROLLBACK TO SAVEPOINT temp_savepoint;")

    def execute_query(self, query: str, params: tuple = ()) -> list[tuple[Any, ...]]:
        """
        Executes a SQL query with parameters and returns a list of query results.

        Args:
            query (str): The SQL query to execute.
            params (tuple): Parameters to bind to the query.

        Returns:
            list[tuple[Any, ...]]: A list of tuples containing the query results.

        Raises:
            sqlite3.Error: If an error occurs during query execution.
        """
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        return result

    def register_custom_function(self, func_name: str, num_args: int,
                                 func: Callable[..., Any]) -> None:
        """
        Registers a custom function for use in SQL queries.

        Args:
            func_name (str): The name of the function to register.
            num_args (int): The number of arguments the function accepts.
            func (Callable[..., Any]): The function implementation.

        Raises:
            sqlite3.Error: If registration fails.
        """
        self.connection.create_function(func_name, num_args, func)
        print(f"Custom function '{func_name}' registered.")


if __name__ == '__main__':
    db_folder = os.path.join(os.path.dirname(__file__), '..', 'database', 'kinodb.db')
    with Database(db_folder) as db:
        print("Starting to create tables.")
        db.create_tables()

        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = db.cursor.fetchall()
        print(f"Current working directory: {os.getcwd()}")
        for table in tables:
            print(f"The table {table[0]} was created")

        movies_data = load_csv('movies.csv')
        print(f"Current working directory: {os.getcwd()}")
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
