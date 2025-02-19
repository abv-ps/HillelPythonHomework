import csv
import sqlite3
from typing import Optional, List, Tuple
from models import Movie, Actor, MovieCast


def connect_db(db_name: str):
    """Функція для підключення до бази даних з обробкою помилок."""
    try:
        # Спробуємо підключитися до бази даних
        conn = sqlite3.connect(db_name)
        print("Database connected successfully.")
        return conn
    except sqlite3.OperationalError as e:
        # Помилка з'єднання, може бути через відсутність бази даних
        print(f"Operational error: {e}. Unable to connect to the database.")
        return None
    except sqlite3.DatabaseError as e:
        # Проблеми з базою даних або доступом до файлу бази даних
        print(f"Database error: {e}. There might be an issue with the database file or permissions.")
        return None
    except sqlite3.Error as e:
        # Загальна помилка, якщо не попали під конкретні випадки
        print(f"An unexpected SQLite error occurred: {e}")
        return None
    except Exception as e:
        # Загальна помилка, якщо виникла інша помилка
        print(f"An unexpected error occurred: {e}")
        return None


def create_tables(cursor: sqlite3.Cursor) -> None:
    """
    Creates tables for movies, actors, and their relationships.
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


def insert_movies(cursor: sqlite3.Cursor, movies: List[Movie]) -> None:
    """
    Inserts movies into the database.

    Args:
        cursor (sqlite3.Cursor): Об'єкт курсора для виконання SQL запитів.
        movies (List[Movie]): Список об'єктів Movie.
    """
    movies_list = [(movie.title, movie.release_year, movie.genre) for movie in movies]

    cursor.executemany('''INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)''', movies_list)


def insert_actors(cursor: sqlite3.Cursor, actors: List[Actor]) -> None:
    """
    Inserts actors into the database.
    """
    actors_list = [(actor.name, actor.birth_year) for actor in actors]

    cursor.executemany('''INSERT INTO actors (name, birth_year) VALUES (?, ?)''', actors_list)


def get_movie_id(cursor: sqlite3.Cursor, title: str) -> Optional[int]:
    """
    Retrieves the movie ID by title.
    """
    cursor.execute("SELECT id FROM movies WHERE title = ?", (title,))
    result = cursor.fetchone()
    return result[0] if result else None


def get_actor_id(cursor: sqlite3.Cursor, name: str) -> Optional[int]:
    """
    Retrieves the actor ID by name.
    """
    cursor.execute("SELECT id FROM actors WHERE name = ?", (name,))
    result = cursor.fetchone()
    return result[0] if result else None


def insert_movie_cast(cursor: sqlite3.Cursor, movie_cast: List[Tuple[int, int]]) -> None:
    """
    Inserts movie-actor relationships into the database.
    """
    cursor.executemany("INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)", movie_cast)


def load_csv(filename: str) -> List[List[str]]:
    """
    Loads a CSV file and returns its content as a list of lists.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data[1:]  # Remove header


if __name__ == '__main__':
    conn = connect_db('kinodb.db')
    local_cursor = conn.cursor()

    create_tables(local_cursor)

    movies_data = load_csv('movies.csv')
    actors_data = load_csv('actors.csv')

    movies_list = [(row[0], int(row[1]), row[2]) for row in movies_data]
    actors_list = [(row[0], int(row[1])) for row in actors_data]

    insert_movies(local_cursor, movies_list)
    insert_actors(local_cursor, actors_list)
    conn.commit()

    movie_cast_data = []
    for movie_title, actor_name in actors_data:
        movie_id = get_movie_id(local_cursor, movie_title)
        actor_id = get_actor_id(local_cursor, actor_name)
        if movie_id and actor_id:
            movie_cast_data.append((movie_id, actor_id))

    insert_movie_cast(local_cursor, movie_cast_data)
    conn.commit()
    conn.close()
    print("Database setup completed successfully!")
