"""
This module provides the MovieService class for managing movie-related operations.

Key Features:
- Searching for movies by keyword (with or without user interaction).
- Inserting new movies while ensuring no duplicates.
- Displaying movies with associated actors using pagination.
- Showing the number of movies by genre.
- Calculating and displaying movie age based on release year.

Usage:
- `MovieService` encapsulates database operations related to movies,
  ensuring better modularity and maintainability.
"""

import datetime
from typing import Optional

from ..database.database_setup import Database as DBClass
from ..database.db_models import Movie, DatabaseHandler as DBHandler
from ..utils.validators import Validator
from ..utils.helpers import (
    choose_page_action,
    handle_no_items_found
)


class MovieService:
    """
    A service class for managing movies, including searching, inserting,
    and displaying movie-related data.
    """

    @staticmethod
    def find_movies_by_keyword(db: DBClass, keyword: str) -> list[tuple[str, int]]:
        """
        Searches for movies by keyword without user interaction.

        Args:
            db (DBClass): The database object for executing SQL queries.
            keyword (str): The keyword to search for in movie titles.

        Returns:
            list[tuple[str, int]]: A list of tuples containing movie titles and release years.
        """
        result = DBHandler.find_by_keyword(
            connection=db.connection,
            table="movies",
            keyword=keyword,
            columns=["title", "release_year"],
            order_by="title"
        )

        return [(movie[0], movie[1]) for movie in result] if result else []

    @staticmethod
    def search_movie_interactive(db: DBClass) -> Optional[str]:
        """
        Prompts the user to search for a movie by a part of its title, using pagination.

        Args:
            db (DBClass): The SQLite database class or cursor object used for executing SQL queries.

        Returns:
            Optional[str]: The title of the movie selected by the user,
                           or None if no valid movie is found.
        """
        from ..ui.movie_database import go_to_main_menu
        movie_name = input("Enter the movie title to search:").strip()
        v = Validator()
        movie_name_sub = v.validate_title_movie(movie_name, "movie title")
        if not movie_name_sub[0]:
            return go_to_main_menu("Movie title is empty")
        movie_name = movie_name_sub[1]

        movies = MovieService.find_movies_by_keyword(db, movie_name)

        if not movies:
            return handle_no_items_found(
                item_name='movie',
                items_func=lambda: MovieService.show_movies_with_actors_with_pagination(db),
                retry_func=lambda: MovieService.search_movie_interactive(db)
            )

        movies_list = [f"{movie[0]} ({movie[1]})" for movie in movies]

        while True:
            action = choose_page_action(
                items=movies_list,
                item_name='found movie'
            )

            if action == "exit":
                return go_to_main_menu("According to your choice 'exit'")

    @staticmethod
    def insert_movie(db: DBClass, movie_title: Optional[str] = None,
                     skip_check: bool = False) -> None:
        """
        Inserts a new movie into the database, ensuring no duplicates.

        Args:
            db (DBClass): The SQLite database class or cursor object used for executing SQL queries.
            movie_title (Optional[str]): The movie title to add. If not provided,
                                         user will be asked to enter it.
            skip_check (bool): Whether to skip the duplicate check. Default is False.

        Returns:
            None: This function does not return a value. It interacts directly with the database
                  and prints status messages.
        """
        from ..ui.movie_database import go_to_main_menu

        if not movie_title:
            movie_title = input("Please enter the movie title to add: ")
            v = Validator()
            movie_name_sub = v.validate_title_movie(movie_title, "movie title")
            if not movie_name_sub[0]:
                return go_to_main_menu("Movie title is empty")
            movie_title = movie_name_sub[1]

        if not skip_check:
            existing_movies = MovieService.find_movies_by_keyword(db, movie_title)
            if existing_movies:
                print(f"Movie '{movie_title}' already exists. Not adding a duplicate.")
                user_choice = input(
                    "Would you like to add another movie? [yes, y, 1] or go back "
                    "to the main menu [no, n]: ").strip().lower()
                if user_choice in ["yes", "y", "1"]:
                    MovieService.insert_movie(db)
                else:
                    return go_to_main_menu("Movie title is empty")

        v = Validator()
        is_valid, release_year = v.validate_year(
            year=int(input("To add the movie to the database, please enter its release year: ")),
            year_type="release"
        )

        if not is_valid:
            return go_to_main_menu("Maximum attempts reached. Invalid input.")

        genre = input("Enter the movie genre: ").strip()
        if not genre:
            genre = input("Genre is not entered. Please enter the movie genre: ").strip()

        if genre:
            genre_sub = v.validate_actor_name_genre(genre, "genre")
            if not genre_sub[0]:
                print(f"The genre {genre_sub[1]} does not meet the requirements, "
                      f"so no genre is added to the movie '{movie_title}'.")
                genre = ''
            else:
                genre = genre_sub[1]

        db.start_savepoint()
        db.insert_movies([Movie(movie_title, release_year, genre)])
        db.release_savepoint()
        movie_id = db.cursor.lastrowid
        print(f"Movie '{movie_title}' with id {movie_id} added.")

        from .actor_service import ActorService
        from ..ui.movie_database import add_reference

        return add_reference(
            db=db,
            item1='actor',
            item2='movie',
            item_id=movie_id,
            func1=ActorService.find_actors_by_keyword
        )

    @staticmethod
    def show_movies_with_actors_with_pagination(db: DBClass, page: int = 1,
                                                page_size: int = 15) -> None:
        """
        Displays all movies and their actors using pagination (15 results per page).

        Args:
            db (DBClass): The database object for executing SQL queries.
            page (int): The current page number (default is 1).
            page_size (int): The number of results per page (default is 15).

        Returns:
            None:
                - This function does not return anything. It prints the movie titles and actors
                  for the current page, and handles pagination and user input for navigation.
        """
        from ..ui.movie_database import go_to_main_menu
        connection = db.connection
        cursor = connection.cursor()

        offset = (page - 1) * page_size

        query = '''
                SELECT m.title, COALESCE(GROUP_CONCAT(a.name, ', '), 'No actors listed') AS actors
                FROM movies m
                LEFT JOIN movie_cast mc ON m.id = mc.movie_id
                LEFT JOIN actors a ON mc.actor_id = a.id
                GROUP BY m.id
                LIMIT ? OFFSET ?
            '''

        cursor.execute(query, (page_size, offset))
        movies_actors = cursor.fetchall()

        cursor.execute('SELECT COUNT(*) FROM movies')
        total_movies = cursor.fetchone()[0]
        total_pages = (total_movies + page_size - 1) // page_size

        if not movies_actors:
            return go_to_main_menu("No movies found on this page.")

        max_title_length = max(len(movie[0]) for movie in movies_actors)

        print(f"Page {page} of {total_pages}\n")
        print(f"Showing movies and actors {offset + 1}-{min(offset + page_size, total_movies)} "
              f"of {total_movies}\n")

        for idx, (movie_title, actors) in enumerate(movies_actors, start=offset + 1):
            padding = ' ' * (max_title_length - len(movie_title) + 4 - len(str(idx)))
            print(f"{idx}. Movie: \"{movie_title}\"{padding}Actors: {actors}")

        if page < total_pages:
            print("Type 'next / +1' to go to the next page.")
        if page > 1:
            print("Type 'prev / -1' to go to the previous page.")
        print("Type 'exit' / 'q' to quit.")

        user_input = input("Your choice: ").strip().lower()

        if user_input in ['next', '+1'] and page < total_pages:
            MovieService.show_movies_with_actors_with_pagination(db, page + 1, page_size)
        elif user_input in ['prev', '-1'] and page > 1:
            MovieService.show_movies_with_actors_with_pagination(db, page - 1, page_size)
        elif user_input in ['exit', 'q']:
            return go_to_main_menu("According to your choice 'exit')")
        else:
            print("\nInvalid input. Please try again.")
            MovieService.show_movies_with_actors_with_pagination(db, page, page_size)

    @staticmethod
    def show_movie_count_by_genre(db: DBClass) -> None:
        """
        Displays the number of movies for each genre.

        Args:
            db (DBClass): The database object for executing SQL queries.

        Returns:
            None:
                - This function does not return anything. It prints the count of
                  movies by genre to the console.
        """
        from .genre_service import GenreService
        from ..ui.movie_database import go_to_main_menu
        genres = GenreService.get_unique_genres(db)

        print("\nMovie count by genre:")
        for genre in genres:
            db.cursor.execute("SELECT COUNT(*) FROM movies WHERE genre = ?", (genre,))
            movie_count = db.cursor.fetchone()[0]

            print(f"Genre: {genre} - {movie_count} {'movie' if movie_count == 1 else 'movies'}")
        return go_to_main_menu()

    @staticmethod
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

    @staticmethod
    def show_movies_with_age(db: DBClass) -> None:

        """
        Displays all movies with their respective ages (years since release).

        Args:
            db (DBClass): The database object to execute SQL queries.

        Returns:
            None:
                - This function does not return anything. It prints the movie titles
                  and their respective ages to the console.
        """
        from ..ui.movie_database import go_to_main_menu
        DBClass.register_custom_function(
            db,
            func_name="movie_age",
            num_args=1,
            func=MovieService.movie_age
        )
        db.cursor.execute("SELECT title, release_year, movie_age(release_year) FROM movies")
        movies = db.cursor.fetchall()

        print("Movies and their age:")
        for i, (movie_title, year, age) in enumerate(movies, 1):
            print(f"{i}. Movie: \"{movie_title}\" ({year}) — {age} {'year' if age == 1 else 'years'}")
        return go_to_main_menu()
