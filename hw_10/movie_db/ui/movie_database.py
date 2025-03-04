"""
This module provides comprehensive functionality for managing and interacting with a movie database.
It supports operations related to movies, actors, and their relationships, as well as offering analytical
queries and user-friendly features for navigating and interacting with the data.

Features:
- Insert new movies and actors into the database.
- Search for movies by title, keyword, or genre with pagination.
- Display all movies along with their respective actors.
- Count and display the number of movies per genre.
- Calculate the age of movies based on their release year.
- Retrieve the average birth year of actors in a given genre.
- Provide pagination for viewing long lists of movies, actors, or genres.
- Search for genres by part of the name.

Functions:
- `find_movies_by_keyword`: Searches for movies based on a keyword.
- `find_actors_by_keyword`: Searches for actors based on a keyword.
- `search_movie_interactive`: Allows interactive search for movies by title.
- `insert_movie`: Adds a new movie to the database.
- `insert_actor`: Adds a new actor to the database and associates them with movies.
- `show_movies_with_actors_with_pagination`: Displays movies with their actors in a paginated format.
- `get_unique_genres`: Retrieves a list of unique movie genres.
- `show_genres`: Displays all movie genres with pagination support.
- `show_movie_count_by_genre`: Displays the count of movies in each genre.
- `movie_age`: Calculates the number of years since a movie's release.
- `show_movies_with_age`: Displays movies along with their respective ages.
- `search_genre_by_part_name`: Prompts the user to search for a genre by part of its name.
- `average_birth_year_of_actors_in_genre`: Computes the average birth year of actors in a particular genre.
- `fetch_actors_and_movies`: Displays actors and their movies in a paginated format using `UNION`.
- `add_reference`: Establishes relationships between movies and actors or other entities.

The program provides an interactive interface to manage a movie database. Users can perform various CRUD operations
such as adding new movies or actors, searching for movies and actors, and viewing detailed analytical information.
Pagination support allows users to easily navigate through large datasets of movies, actors, and genres.
"""
import os
import sys
from typing import Callable, Any

from ..database.database_setup import Database as DBClass
from ..database.db_models import MovieCast, DatabaseHandler as DBHandler
from ..utils.helpers import choose_page_action
from ..services.actor_service import ActorService
from ..services.movie_service import MovieService
from ..services.genre_service import GenreService


def average_birth_year_of_actors_in_genre(db: DBClass) -> float | None:
    """
    Displays the average birth year of actors in movies of a specific genre.

    Args:
        db (DBClass): The database object to execute SQL queries.

    Returns:
        float | None:
            - The average birth year of actors in the specified genre, rounded to the nearest integer.
            - None if no actors are found for the specified genre.
    """
    genre = GenreService.search_genre_by_part_name(db, selection='on')
    query = """
        SELECT AVG(a.birth_year)
        FROM actors a
        JOIN movie_cast mc ON a.id = mc.actor_id
        JOIN movies m ON mc.movie_id = m.id
        WHERE m.genre = ?
    """
    result = db.execute_query(query, (genre,))
    average_birth_year = result[0][0] if result and result[0][0] is not None else None

    if not average_birth_year:
        return go_to_main_menu(f"No actors found for genre: {genre}")

    return go_to_main_menu(f"Average birth year of actors in movies of genre "
                           f"'{genre}' is {average_birth_year:.0f}")


def fetch_actors_and_movies(db: DBClass) -> None:
    """
    Fetches and displays names of all actors and movie titles in a paginated format using UNION.

    This function retrieves both actors and movies from the database, displaying their names and birth years
    in a paginated format. The results are ordered by type (Actor or Film), name, and year.

    Args:
        db (DBClass): The database object to execute SQL queries.
                      It is expected to have an `execute_query` method to run the SQL query and return the results.

    Returns:
        None: This function does not return any value. It displays the result in a paginated format
              and provides an option to navigate through pages.
    """
    query = """
        SELECT name AS result, birth_year AS year, 'Actor' AS type FROM actors
        UNION
        SELECT title AS result, release_year AS year, 'Film' AS type FROM movies
        ORDER BY type, result, year;
    """
    raw_results = db.execute_query(query)

    results = [f"{row[2]}: {row[0]} ({row[1]})" for row in raw_results]

    choose_page_action(
        current_page=1,
        items=results,
        item_name="actors and movies",
        selection='off'
    )
    return go_to_main_menu()


def add_reference(
        db: DBClass,
        item1: str,
        item2: str,
        item_id: int | None,
        func1: Callable[[DBClass, str], list[tuple[str, int]]],
) -> None:
    """
    Prompts the user to add a reference between two items in the database.

    This function interacts with the user to add a reference between two items in the database.
    It allows searching for an existing item or adding a new one if it does not exist in the database.
    Once a valid reference is found or created, the function inserts the reference into the database.

    Args:
        db (DBClass): The database object, used for executing SQL queries and retrieving data.
        item1 (str): The name of the first item to add reference (e.g., "actor").
        item2 (str): The name of the second item to add reference (e.g., "movie").
        item_id (int | None): The ID of the second item (e.g., movie ID) that will be referenced.
        func1 (Callable[[DBClass, str], list[tuple[str, int]]]): Function to search for the first item in the database.

    Returns:
        None: The function does not return any value, but prompts the user and inserts a reference into the database.
    """
    add_ref = input(f"Would you like to add a {item1} reference to this {item2}? "
                    f"[yes, y, 1] or go back to the main menu [no, n]: ").strip().lower()

    if add_ref not in ["yes", "y", "1"]:
        return go_to_main_menu("According to your choice 'exit'")

    item_part = input(f"Please enter the {item1} to search in database: ")
    search_results = func1(db, item_part)
    print(f"{item2} (id is {item_id})")
    if search_results:
        search_item1 = [item[0] for item in search_results]

        if len(search_item1) > 1:
            selection = choose_page_action(
                items=search_item1,
                item_name=f"found {item1}",
                selection='on'
            )
            if selection == "exit":
                return go_to_main_menu("According to your choice 'exit'")
            search_item1 = selection
        else:
            search_item1 = search_item1[0]
    else:
        add_new_item1 = input(
            f"There is no such {item1} in the database, would you like to add a {item1}? [yes, y, 1]: ").strip().lower()
        if add_new_item1 in ["yes", "y", "1"]:
            item2_name = DBHandler.get_name_by_id(db.connection, item2, item_id)
            if item1 == "actor":
                ActorService.insert_actor(db=db, movie_title=item2_name, actor_name=item_part)
            else:
                MovieService.insert_movie(db=db, movie_title=item_part, skip_check=True)
            search_results = func1(db, item_part)
            if not search_results:
                return go_to_main_menu(f"Failed to add {item1}.")
            search_item1 = search_results[0]
        else:
            print(f"{item1.capitalize()} was not added. {item2.capitalize()} remains unlinked.")
            return go_to_main_menu()

    get_id_func = getattr(DBClass, f"get_{item1}_id", None)
    if get_id_func:
        item1_id = get_id_func(db, search_item1)
        if item1_id:
            moviecast_list = [MovieCast(item1_id, item_id)]
            db.start_savepoint()
            db.insert_movie_cast(moviecast_list)
            db.release_savepoint()
            print(f"Reference between {item1} {search_item1} and {item2} "
                  f"{DBHandler.get_name_by_id(db.connection, item2, item_id)} "
                  f"added successfully.")
    return go_to_main_menu()


def go_to_main_menu(prompt_message: str = None) -> None:
    """
    Prompts the user to return to the main menu and handles the user input.

    Args:
        prompt_message (str, optional): The message that will be shown to the user.
                                         If not provided, no prompt will be displayed.
    """
    if prompt_message and prompt_message != "According to your choice 'exit'":
        user_input = input(f"{prompt_message}\nType something and press Enter to join the main menu: ")
    elif not prompt_message:
        user_input = input("Type something and press Enter to join the main menu: ")
    else:
        print(prompt_message)

    print("Returning to the main menu...")
    return None


def exit_program() -> None:
    """
    Prints a message indicating the program is finishing and exits the program.

    This function is typically used to terminate the program, displaying a
    farewell message to the user before calling sys.exit(0) to end the process.

    Returns:
        None: This function does not return any value. It exits the program.
    """
    print("Finishing work with database... Thank you, have a nice to meet!")
    sys.exit(0)


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
    # db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'kinodb.db')
    # db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'database', 'kinodb.db')
    db_path = r"C:\Users\Bogdan\PycharmProjects\HillelPythonHomework\hw_10\movie_db\database\kinodb.db"
    with DBClass(db_path) as db:
        options = {
            "1": MovieService.insert_movie,
            "2": ActorService.insert_actor,
            "3": MovieService.search_movie_interactive,
            "4": MovieService.show_movies_with_actors_with_pagination,
            "5": GenreService.show_genres,
            "6": MovieService.show_movie_count_by_genre,
            "7": MovieService.show_movies_with_age,
            "8": GenreService.search_genre_by_part_name,
            "9": average_birth_year_of_actors_in_genre,
            "10": fetch_actors_and_movies,
            "0": exit_program
        }

        while True:
            print("Hello! Welcome to the movie database menu. How would you like to proceed?")
            print("\n1. Add Movie\n2. Add Actor\n3. Search Movie by keyword"
                  "\n4. Show all movies with actors (with pagination)\n5. Show all genres"
                  "\n6. Show movie count by genre\n7. Show movies with age"
                  "\n8. Search genre by part name\n9. Show average birth year of actors in genre"
                  "\n10. Show names of all actors and titles of all movies\n0. Exit")
            choice = input("Choose an option: ")

            if choice in options:
                if choice != "0":
                    options[choice](db)
                else:
                    options[choice]()
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
