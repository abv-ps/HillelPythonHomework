"""
This module provides functionality for interacting with a movie database, including operations
for managing movies, actors, and their relationships. The module supports various CRUD operations,
including inserting, searching, and displaying data, as well as performing analytical queries.

Features:
- Insert new movies and actors into the database.
- Search for movies by title or genre with pagination.
- Show all movies with their actors.
- Display the count of movies per genre.
- Calculate the age of movies (years since release).
- Fetch the average birth year of actors in a specific genre.
- Show movies along with actors in a paginated format.
- Provide pagination for viewing long lists of items (movies, actors, genres).

Functions:
- `choose_page_action`: Handles pagination and item selection.
- `find_movies_by_keyword`: Searches for movies based on a keyword.
- `search_movie_interactive`: Allows interactive movie search by title.
- `insert_movie`: Adds a new movie to the database.
- `insert_actor`: Adds a new actor and associates them with movies.
- `show_movies_with_actors`: Displays movies with their actors in a paginated list.
- `get_unique_genres`: Retrieves a list of unique movie genres.
- `show_genre`: Displays movie genres with pagination.
- `show_movie_count_by_genre`: Displays the number of movies per genre.
- `movie_age`: Calculates the number of years since a movie's release.
- `register_functions`: Registers custom SQLite functions.
- `show_movies_with_age`: Displays movies with their ages.
- `search_genre_by_part_name`: Prompts the user to search for a genre by name.
- `average_birth_year_of_actors_in_genre`: Displays the average birth year of actors in a specific genre.
- `fetch_actors_and_movies`: Displays actors and movies in a paginated format using `UNION`.

The program allows users to interactively add and manage movies and actors, perform various searches, and view
analytical results in a user-friendly manner with pagination support.

"""

import sqlite3
import datetime
from typing import Optional, List, Tuple
from database_setup import (
    connect_db,
    insert_movies,
    insert_actors,
    insert_movie_cast
)
from models import Movie, Actor, MovieCast
from hw_10.database_setup import get_actor_id, get_movie_id


def choose_page_action(current_page: int, total_pages: int, items: list, item_name: str,
                       results_per_page: int = 15) -> str | int:
    """
    Prompts the user to choose an item or navigate between pages (next, prev).

    Args:
        current_page (int): The current page number.
        total_pages (int): The total number of pages.
        items (list): The list of items to select from (e.g., movies, actors).
        item_name (str): The name of the item (e.g., "movie", "actor").
        results_per_page (int): The number of items to display per page (default is 15).

    Returns:
        str|int: The name of the selected item or the new current page number if user navigates between pages.
    """
    while True:
        start_index = (current_page - 1) * results_per_page
        end_index = start_index + results_per_page
        page_items = items[start_index:end_index]

        print(f"Page {current_page} of {total_pages}\n")
        print(f"Showing {item_name}s {start_index + 1}-{start_index + len(page_items)} of {len(items)}")

        for i, item in enumerate(page_items, 1):
            print(f"{start_index + i}. {item}")

        print("\nTo return to the main menu, type 'exit' or 'q'.")

        choice = input(
            f"Select a {item_name} (1-{len(page_items)}) or type 'next'|'+1' to go to the next page, "
            f"type 'prev'|'-1' to go to the previous page: ").strip().lower()

        if choice in {"exit", "q"}:
            return "exit"

        if choice.isdigit():
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(page_items):
                return page_items[choice_index][0]
            print("Invalid selection. Please try again.")
        elif choice in ['next', '+1']:
            if current_page < total_pages:
                return current_page + 1
            print("You are already on the last page.")
        elif choice in ['prev', '-1']:
            if current_page > 1:
                return current_page - 1
            print("You are already on the first page.")


def find_movies_by_keyword(cursor: sqlite3.Cursor, keyword: str) -> List[Tuple[str]]:
    """
    Searches for movies by keyword without user interaction.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
        keyword (str): The keyword to search for in movie titles.

    Returns:
        List[Tuple[str]]: A list of movie titles matching the keyword.
    """
    cursor.execute("SELECT title FROM movies WHERE LOWER(title) LIKE LOWER(?) ORDER BY title",
                   (f"%{keyword}%",))
    return cursor.fetchall()


def search_movie_interactive(cursor: sqlite3.Cursor) -> Optional[str]:
    """
    Prompts the user to search for a movie by a part of its title, using pagination.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.

    Returns:
        Optional[str]: The title of the movie selected by the user, or None if no valid movie is found.
    """
    attempts = 0
    results_per_page = 15
    while attempts < 3:
        movie_name = input("Enter a part of the movie title to search for: ")
        movies = find_movies_by_keyword(cursor, movie_name)

        if not movies:
            print("No movies found with that title.")
            attempts += 1
            continue

        total_pages = (len(movies) + results_per_page - 1) // results_per_page
        current_page = 1
        item_name = 'movie'

        while True:
            film_or_page = choose_page_action(current_page, total_pages, movies, item_name, results_per_page)

            if isinstance(film_or_page, str):
                if film_or_page == "exit":
                    return None
                return film_or_page
            current_page = film_or_page

    print("Too many invalid attempts. Exiting...")
    return None


def insert_movie(cursor: sqlite3.Cursor, movie_name: str|None = None, skip_check: bool = False) -> None:
    """
    Inserts a new movie into the database, ensuring no duplicates.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
        movie_name (Optional[str]): The movie title to add. If not provided, user will be asked to enter it.
        skip_check (bool): Whether to skip the duplicate check. Default is False.
    """
    if not movie_name:
        movie_name = input("Enter the movie title to add: ")
    if not skip_check:
        existing_movies = find_movies_by_keyword(cursor, movie_name)
        if any(movie[0].lower() == movie_name.lower() for movie in existing_movies):
            print(f"Movie '{movie_name}' already exists. Not adding a duplicate.")
            return

    for _ in range(3):
        try:
            release_year = int(input("Enter the movie release year: "))
            if 1900 <= release_year <= 2100:
                break
            print("Please enter a valid year between 1900 and 2100.")
        except ValueError:
            print("Invalid release year. Please enter a valid number.")
    else:
        print("Too many invalid attempts. Exiting...")
        return

    genre = input("Enter the movie genre: ")
    if not genre:  # Якщо введено порожній рядок
        genre = input("Genre is not entered. Please enter the movie genre:")

    insert_movies(cursor, [Movie(movie_name, release_year, genre)])
    cursor.connection.commit()
    print(f"Movie '{movie_name}' added.")


def insert_actor(cursor: sqlite3.Cursor) -> None:
    """
    Inserts a new actor into the database and associates them with movies.

    Args:
        cursor (sqlite3.Cursor): The SQLite database cursor.
    """
    actor_name = input("Enter the actor's name: ")

    existing_actor = get_actor_id(cursor, actor_name)
    if not existing_actor:
        for _ in range(3):
            try:
                birth_year = int(input("Enter the actor's birth year: "))
                break
            except ValueError:
                print("Invalid birth year. Please enter a valid number.")
        else:
            print("Too many invalid attempts. Exiting...")
            return

        insert_actors(cursor, [Actor(actor_name, birth_year)])
        actor_id = cursor.lastrowid
        cursor.connection.commit()
        print(f"Actor '{actor_name}' added.")
    else:
        actor_id = existing_actor

    add_film = input("Would you like to add a movie reference to this actor?"
                     " [yes, y, 1]: ").strip().lower()
    if add_film in ["yes", "y", "1"]:
        movie_title = search_movie_interactive(cursor)

        if not movie_title:
            add_new_movie = input("There is no such movie in the database, would you like to add a movie?"
                                  " [yes, y, 1]: ").strip().lower()
            if add_new_movie in ["yes", "y", "1"]:
                insert_movie(cursor, movie_title, skip_check=True)
                return
            print("Movie was not added. Actor remains unlinked.")

        movie_id = get_movie_id(cursor, movie_title)
        cursor.execute("SELECT 1 FROM movie_cast WHERE movie_id = ? AND actor_id = ?",
                       (movie_id, actor_id))
        if cursor.fetchone():
            print(f"Actor '{actor_name}' is already associated with '{movie_title}'.")
        else:
            insert_movie_cast(cursor, [MovieCast(movie_id, actor_id)])
            cursor.connection.commit()
            print(f"Actor '{actor_name}' added to '{movie_title}'.")


def show_movies_with_actors(cursor: sqlite3.Cursor) -> None:
    """
    Displays all movies and their actors using pagination (15 results per page).

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
    """
    current_page = 1
    page_size = 15

    # Get the total count of movies for pagination
    cursor.execute("SELECT COUNT(*) FROM movies")
    total_movies = cursor.fetchone()[0]
    total_pages = (total_movies + page_size - 1) // page_size

    while True:
        offset = (current_page - 1) * page_size

        cursor.execute('''
            SELECT m.title, COALESCE(GROUP_CONCAT(a.name, ', '), 'No actors listed') AS actors
            FROM movies m
            LEFT JOIN movie_cast mc ON m.id = mc.movie_id
            LEFT JOIN actors a ON mc.actor_id = a.id
            GROUP BY m.id
            LIMIT ? OFFSET ?
        ''', (page_size, offset))

        movies_actors = cursor.fetchall()

        if not movies_actors:
            print("No more movies available.")
            break

        formatted_movies = [
            f"{(current_page - 1) * page_size + i}. Movie: \"{movie_title}\", Actors: {actors}"
            for i, (movie_title, actors) in enumerate(movies_actors, 1)
        ]

        selected = choose_page_action(current_page, total_pages, formatted_movies, "movie", page_size)

        if isinstance(selected, str):  # Вибір фільму
            if selected == "exit":  # Якщо користувач обрав exit
                return
            movie_index = int(selected.split(".")[0]) - 1  # Отримуємо індекс фільму
            movie_title = movies_actors[movie_index][0]
            print(f"You selected the movie: {movie_title}")
            break

        if isinstance(selected, int):  # Перехід між сторінками
            current_page = selected


def get_unique_genres(cursor: sqlite3.Cursor) -> list:
    """
    Retrieves all unique movie genres from the database.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.

    Returns:
        list: A list of unique movie genres.
    """
    cursor.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
    return [genre[0] for genre in cursor.fetchall()]


def show_genres(cursor: sqlite3.Cursor) -> int | str | None:
    """
    Displays a list of all unique movie genres with pagination (15 genres per page)
    and allows the user to navigate through the pages.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.

    Returns:
        int | str | None:
            - int if user selects a new page
            - str if user selects a genre
            - None if the user exits
    """
    genres = get_unique_genres(cursor)
    results_per_page = 15

    if not genres:
        print("No genres found.")
        return None

    total_pages = (len(genres) + results_per_page - 1) // results_per_page
    current_page = 1

    while True:
        selected = choose_page_action(current_page, total_pages, genres, "genre", results_per_page)

        if selected == "exit":
            return None  # Returning None if the user exits

        if isinstance(selected, int):
            current_page = selected
        else:
            print(f"You selected the genre: {selected}")
            return selected  # Returning the selected genre


def show_movie_count_by_genre(cursor: sqlite3.Cursor) -> None:
    """
    Displays the number of movies for each genre.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
    """
    genres = get_unique_genres(cursor)

    if not genres:
        print("No genres found.")
        return

    print("\nMovie count by genre:")
    for genre, in genres:
        # Get the count of movies for each genre
        cursor.execute("SELECT COUNT(*) FROM movies WHERE genre = ?", (genre,))
        movie_count = cursor.fetchone()[0]

        print(f"Genre: {genre} - {movie_count} movies")


def movie_age(release_year: int) -> int:
    """
    Calculates the age of a movie based on its release year.

    Args:
        release_year (int): The release year of the movie.

    Returns:
        int: The number of years since the movie's release.
    """
    current_year = datetime.datetime.now().year
    return current_year - release_year


def register_functions(conn):
    """Реєструє кастомну функцію в SQLite."""
    conn.create_function("movie_age", 1, movie_age)


def show_movies_with_age(cursor: sqlite3.Cursor) -> None:
    """
    Displays all movies with their respective ages (years since release).

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
    """
    cursor.execute("SELECT title, release_year, movie_age(release_year) FROM movies")
    movies = cursor.fetchall()

    if not movies:
        print("No movies found.")
        return

    print("Movies and their age:")
    for i, (movie_title, release_year) in enumerate(movies, 1):
        age = movie_age(release_year)  # Calculate movie age
        print(f"{i}. Movie: \"{movie_title}\" — {age} years")


def search_genre_by_part_name(cursor: sqlite3.Cursor) -> str | None:
    """
    Prompts the user to enter a part of a genre name and returns the genre that matches the search.

    If no results are found, asks the user if they want to see all genres.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.

    Returns:
        str: The genre selected by the user, or None if not found.
    """
    attempts = 0
    while attempts < 3:
        genre_part = input("Enter part of the genre name to search for "
                           "(or 'exit'/'q' to return to the main menu): ").strip()

        if genre_part in ['exit', 'q']:
            print("Returning to the main menu...")
            return None

        # Fetch genres that match the entered part of the genre name
        cursor.execute("SELECT DISTINCT genre FROM movies WHERE genre LIKE ?", (f"%{genre_part}%",))
        genres = cursor.fetchall()

        if genres:
            print(f"Found genres: {[genre[0] for genre in genres]}")
            genre_choice = input("Select a genre from the above list: ").strip()
            if genre_choice in [genre[0] for genre in genres]:
                return genre_choice
            print("Invalid genre selection. Try again.")
            attempts += 1
        else:
            print("No genres found with that name.")
            retry_choice = input("Would you like to see all genres? [yes, y, 1]"
                                 "(or 'exit'/'q' to return to the main menu): ").strip().lower()
            if retry_choice in ['exit', 'q']:
                print("Returning to the main menu...")
                return None
            if retry_choice in ['yes', 'y', '1']:
                return str(show_genres(cursor))
            print("You can try again.")
            attempts += 1

    print("Too many invalid attempts. Exiting...")
    return None


def average_birth_year_of_actors_in_genre(cursor: sqlite3.Cursor, genre: str) -> float | None:
    """
    Displays the average birth year of actors in movies of a specific genre.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
        genre (str): The genre of the movies to filter by.

    Returns:
        float: The average birth year of actors.
    """
    cursor.execute("""
        SELECT AVG(a.birth_year)
        FROM actors a
        JOIN movie_cast mc ON a.id = mc.actor_id
        JOIN movies m ON mc.movie_id = m.id
        WHERE m.genre = ?
    """, (genre,))
    average_birth_year = cursor.fetchone()[0]

    if not average_birth_year:
        print(f"No actors found for genre: {genre}")
        return None
    print(f"Average birth year of actors in movies of genre '{genre}' is {average_birth_year:.0f}")
    return average_birth_year


def fetch_actors_and_movies(cursor: sqlite3.Cursor, results_per_page: int = 10) -> None:
    """
    Fetches and displays names of all actors and movie titles in a paginated format using UNION.

    Args:
        cursor (sqlite3.Cursor): The database cursor to execute queries.
        results_per_page (int): Number of results to show per page.
    """
    cursor.execute("""
            SELECT name AS result FROM actors
            UNION
            SELECT title AS result FROM movies
            ORDER BY result;
        """)

    results = [row[0] for row in cursor.fetchall()]
    total_results = len(results)
    total_pages = (total_results + results_per_page - 1) // results_per_page
    current_page = 1

    while True:
        action = choose_page_action(current_page, total_pages, results, "result", results_per_page)

        if action == "exit":
            break
        if isinstance(action, int):
            current_page = action
        else:
            print(f"You selected: {action}")
            break


def main():
    """
    Main function for managing the movie database application.

    This function handles the user interface, allowing the user to choose
    different actions related to movie and actor management. The user can:
    - Add a new movie.
    - Add a new actor.
    - Search for movies by keyword.
    - Display all movies with actors.
    - Show a list of all genres.
    - Show the count of movies by genre.
    - Display movies with a certain age rating.
    - Search genres by part of the name.
    - Show the average birth year of actors in a genre.
    - Display names of all actors and titles of all movies.

    The user can choose an action by inputting a corresponding number.
    The program will continue until the user chooses the "Exit" option (option 0).
    """
    with connect_db("movies.db") as conn:
        cursor = conn.cursor()
        register_functions(conn)
        options = {
            "1": insert_movie,
            "2": insert_actor,
            "3": search_movie_interactive,
            "4": show_movies_with_actors,
            "5": show_genres,
            "6": show_movie_count_by_genre,
            "7": show_movies_with_age,
            "8": search_genre_by_part_name,
            "9": average_birth_year_of_actors_in_genre,
            "10": fetch_actors_and_movies,
            "0": lambda: None  # Для виходу з програми
        }

        while True:
            print("\n1. Add Movie\n2. Add Actor\n3. Search Movie by keyword"
                  "\n4. Show all movies with actors\n5. Show all genres"
                  "\n6. Show movie count by genre\n7. Show movies with age"
                  "\n8. Search genre by part name\n9. Show average birth year of actors in genre"
                  "\10. Show names of all actors and titles of all movies\n0. Exit")
            choice = input("Choose an option: ")

            if choice in options:
                if choice == "9":
                    # Спеціальний випадок, де потрібно двічі викликати функцію
                    genre = search_genre_by_part_name(cursor)
                    options[choice](cursor, genre)
                elif choice == "8":
                    # Можливо, вам потрібно буде обробляти специфічні випадки
                    options[choice](cursor)
                else:
                    options[choice](cursor)
            else:
                print("Invalid choice. Try again.")

            if choice == "0":
                break


if __name__ == "__main__":
    main()
