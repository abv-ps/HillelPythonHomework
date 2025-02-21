"""
This module handles the setup and initialization of a SQLite database for storing movie data, including movies, actors, and their relationships.

Functions:
- connect_db(db_name: str): Establishes a connection to the SQLite database.
- create_tables(cursor: sqlite3.Cursor): Creates the necessary tables for storing movie, actor, and movie-actor relationship data.
- insert_movies(cursor: sqlite3.Cursor, movies: list[Movie]): Inserts a list of Movie objects into the database.
- insert_actors(cursor: sqlite3.Cursor, actors: list[Actor]): Inserts a list of Actor objects into the database.
- get_movie_id(cursor: sqlite3.Cursor, title: str): Retrieves the ID of a movie by its title.
- get_actor_id(cursor: sqlite3.Cursor, name: str): Retrieves the ID of an actor by their name.
- insert_movie_cast(cursor: sqlite3.Cursor, movie_cast: list[MovieCast]): Inserts a list of MovieCast objects into the database to establish relationships between movies and actors.
- load_csv(filename: str): Loads data from a CSV file and returns it as a list of rows, excluding the header.

This module is designed to be run as a standalone script that will:
1. Connect to the SQLite database.
2. Create necessary tables if they do not exist.
3. Load data from CSV files (movies, actors, and movie-actor relationships).
4. Insert the loaded data into the database.
5. Commit changes and close the connection to the database.
"""

import sys
import csv
import sqlite3
from typing import Optional
from models import Movie, Actor, MovieCast


def connect_db(db_name: str) -> Optional[sqlite3.Connection]:
    """
    Establishes a connection to the SQLite database.

    Args:
        db_name (str): The name of the database file.

    Returns:
        Optional[sqlite3.Connection]: The database connection object if successful, otherwise None.
    """
    try:
        connection = sqlite3.connect(db_name)
        print("Database connected successfully.")
        return connection
    except sqlite3.OperationalError as e:
        print(f"Operational error: {e}. Unable to connect to the database.")
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}. Check the database file or permissions.")
    except sqlite3.Error as e:
        print(f"Unexpected SQLite error: {e}")
    return None


def create_tables(cursor: sqlite3.Cursor) -> None:
    """
    Creates tables for movies, actors, and their relationships if they do not exist.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object for executing queries.
    """
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.executescript('''
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


def insert_movies(cursor: sqlite3.Cursor, movies: list[Movie]) -> None:
    """
    Inserts a list of movies into the database.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object.
        movies (list[Movie]): List of Movie objects.
    """
    movie_data = [(movie.title, movie.release_year, movie.genre) for movie in movies]
    cursor.executemany("INSERT INTO movies (title, release_year, genre) "
                       "VALUES (?, ?, ?)", movie_data)


def insert_actors(cursor: sqlite3.Cursor, actors: list[Actor]) -> None:
    """
    Inserts a list of actors into the database.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object.
        actors (list[Actor]): List of Actor objects.
    """
    actor_data = [(actor.name, actor.birth_year) for actor in actors]
    cursor.executemany("INSERT INTO actors (name, birth_year) VALUES (?, ?)", actor_data)


def get_movie_id(cursor: sqlite3.Cursor, title: str) -> Optional[int]:
    """
    Retrieves the movie ID by title.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object.
        title (str): The title of the movie.

    Returns:
        Optional[int]: The ID of the movie if found, otherwise None.
    """
    cursor.execute("SELECT id FROM movies WHERE title = ?", (title,))
    result = cursor.fetchone()
    return result[0] if result else None


def get_actor_id(cursor: sqlite3.Cursor, name: str) -> Optional[int]:
    """
    Retrieves the actor ID by name.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object.
        name (str): The name of the actor.

    Returns:
        Optional[int]: The ID of the actor if found, otherwise None.
    """
    cursor.execute("SELECT id FROM actors WHERE name = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else None


def insert_movie_cast(cursor: sqlite3.Cursor, movie_cast: list[MovieCast]) -> None:
    """
    Inserts movie-actor relationships into the database.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object.
        movie_cast (list[MovieCast]): List of MovieCast objects.
    """
    cast_data = [(cast.movie_id, cast.actor_id) for cast in movie_cast]
    cursor.executemany("INSERT OR IGNORE INTO movie_cast (movie_id, actor_id) VALUES (?, ?)", cast_data)


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
    return data[1:]  # Exclude header


if __name__ == '__main__':
    conn = connect_db('kinodb.db')
    if conn is None:
        print("Failed to connect to the database. Exiting...")
        sys.exit(1)
    local_cursor = conn.cursor()

    create_tables(local_cursor)

    movies_data = load_csv('movies.csv')
    actors_data = load_csv('actors.csv')

    movies_list = [Movie(row[0], int(row[1]), row[2]) for row in movies_data]
    actors_list = [Actor(row[1], int(row[2])) for row in actors_data]

    insert_movies(local_cursor, movies_list)
    insert_actors(local_cursor, actors_list)
    conn.commit()

    movie_cast_list = []
    for title, name, _ in actors_data:
        movie_id = get_movie_id(local_cursor, title)
        actor_id = get_actor_id(local_cursor, name)
        if movie_id and actor_id:
            movie_cast_list.append(MovieCast(movie_id, actor_id))

    insert_movie_cast(local_cursor, movie_cast_list)
    conn.commit()
    conn.close()
    print("Database setup completed successfully!")
