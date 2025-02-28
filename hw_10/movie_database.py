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
- `find_movies_by_keyword`: Searches for movies based on a keyword.
- `search_movie_interactive`: Allows interactive movie search by title.
- `insert_movie`: Adds a new movie to the database.
- `insert_actor`: Adds a new actor and associates them with movies.
- `show_movies_with_actors_with_pagination`: Displays movies with their actors in a paginated list.
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

import sys
import datetime
from typing import Optional, Callable, Any
from database_setup import Database as DBClass
from db_models import (
    Movie,
    Actor,
    MovieCast,
    DatabaseHandler as DBHandler
)
from services import (
    Validator,
    choose_page_action,
    go_to_main_menu,
    case_insensitive_collation,
    handle_no_items_found
)


def find_movies_by_keyword(db: DBClass, keyword: str) -> list[tuple[str, int]]:
    """
    Searches for movies by keyword without user interaction.

    Args:
        db (DBClass): The Database object for executing SQL queries.
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


def find_actors_by_keyword(db: DBClass, keyword: str) -> list[tuple[str, int]]:
    """
    Searches for actors by keyword without user interaction.

    Args:
        db (DBClass): The Database object for executing SQL queries.
        keyword (str): The keyword to search for in movie titles.

    Returns:
        list[tuple[str, int]]: A list of tuples containing movie titles and release years.
    """
    result = DBHandler.find_by_keyword(
        connection=db.connection,
        table="actors",
        keyword=keyword,
        columns=["name", "birth_year"],
        order_by="name"
    )

    return list(set((actor[0], actor[1]) for actor in result)) if result else []


def search_movie_interactive(db: DBClass) -> Optional[str]:
    """
    Prompts the user to search for a movie by a part of its title, using pagination.

    Args:
        db: Database : The db: Database object for executing SQL queries.

    Returns:
        Optional[str]: The title of the movie selected by the user, or None if no valid movie is found.
    """
    movie_name = input("Enter the movie title to search:").strip()
    v = Validator()
    movie_name_sub = v.validate_title_movie(movie_name, "movie title")
    if not movie_name_sub[0]:
        return go_to_main_menu()
    else:
        movie_name = movie_name_sub[1]

    movies = find_movies_by_keyword(db, movie_name)

    if not movies:
        return handle_no_items_found(
            item_name='movie',
            items_func=show_movies_with_actors_with_pagination(db),
            retry_func=search_movie_interactive(db)
        )

    movies_list = [f"{movie[0]} ({movie[1]})" for movie in movies]

    while True:
        action = choose_page_action(
            items=movies_list,
            item_name='found movie'
        )

        if action == "exit":
            return go_to_main_menu()


def insert_movie(db: DBClass, movie_name: str | None = None, skip_check: bool = False) -> None:
    """
    Inserts a new movie into the database, ensuring no duplicates.

    Args:
        db: Database : The db: Database object for executing SQL queries.
        movie_name (Optional[str]): The movie title to add. If not provided, user will be asked to enter it.
        skip_check (bool): Whether to skip the duplicate check. Default is False.
    """
    if not movie_name:
        movie_name = input("Please enter the movie title to add: ")
        v = Validator()
        movie_name_sub = v.validate_title_movie(movie_name, "movie title")
        if not movie_name_sub[0]:
            return go_to_main_menu()
        else:
            movie_name = movie_name_sub[1]

    if not skip_check:
        existing_movies = find_movies_by_keyword(db, movie_name)
        if existing_movies:
            print(f"Movie '{movie_name}' already exists. Not adding a duplicate.")
            user_choice = input(
                "Would you like to add another movie? [yes, y, 1] or go back to the main menu [no, n]: ").strip().lower()
            if user_choice in ["yes", "y", "1"]:
                insert_movie(db)
            else:
                return go_to_main_menu()

    for _ in range(3):
        try:
            release_year = int(input("To add the movie to the database, "
                                     "please enter its release year: "))
            if 1900 <= release_year <= 2100:
                break
            print("Please enter a valid year between 1900 and 2100.")
        except ValueError:
            print("Invalid release year. Please enter a valid number.")
    else:
        print("Maximum attempts reached. Invalid input.")
        return go_to_main_menu()

    genre = input("Enter the movie genre: ")
    if not genre:
        genre = input("Genre is not entered. Please enter the movie genre:")
    if genre:
        v = Validator()
        genre_sub = v.validate_actor_name_genre(genre, "genre")
        if not genre_sub[0]:
            print(f"The genre {genre_sub[1]} does not meet the requirements, "
                  f"so no genre is added to the movie '{movie_name}'.")
            genre = ''
        else:
            genre = genre_sub[1]
    db.start_savepoint()
    db.insert_movies([Movie(movie_name, release_year, genre)])
    movie_id = db.cursor.lastrowid
    db.release_savepoint()
    print(f"Movie '{movie_name}' added.")
    add_reference(
        db=db,
        item1='actor',
        item2='movie',
        item_id=movie_id,
        func1=lambda db, keyword: find_actors_by_keyword(db, keyword),
        func2=lambda: insert_actor(db, movie_name),
        insert_func=lambda movie_cast: db.insert_movie_cast(movie_cast)
    )


def insert_actor(db: DBClass, movie_name: str | None = None) -> None:
    """
    Inserts a new actor into the database and associates them with movies.

    Args:
        db: Database (sqlite3.Cursor): The SQLite database db: Database.
    """
    actor_name = input("Enter the actor's name: ")
    v = Validator()
    actor_name_sub = v.validate_actor_name_genre(actor_name, "actor's name")
    if not actor_name_sub[0]:
        return go_to_main_menu()
    else:
        actor_name = actor_name_sub[1]
    existing_actor = db.get_actor_id(actor_name)
    if not existing_actor:
        for _ in range(3):
            try:
                birth_year = int(input("Enter the actor's birth year: "))
                if 1900 <= birth_year <= 2100:
                    break
                print("Please enter a valid year between 1900 and 2100.")
            except ValueError:
                print("Invalid birth year. Please enter a valid number.")
        else:
            print("Too many invalid attempts. Exiting...")
            return

        db.start_savepoint()
        db.insert_actors([Actor(actor_name, birth_year)])
        actor_id = db.cursor.lastrowid
        db.release_savepoint()
        print(f"Actor '{actor_name}' added.")
    else:
        actor_id = existing_actor

    add_reference(
        db=db,
        item1='movie',
        item2='actor',
        item_id=actor_id,
        func1=lambda db, keyword: find_movies_by_keyword(db, keyword),
        func2=lambda: insert_movie(db, movie_name),
        insert_func=lambda movie_cast: db.insert_movie_cast(movie_cast)
    )


def show_movies_with_actors_with_pagination(db: DBClass, page: int = 1,
                                            page_size: int = 15) -> None:
    """
    Displays all movies and their actors using pagination (15 results per page).

    Args:
        db: Database (sqlite3.Cursor): The db: Database object for executing SQL queries.
    """
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
        print("No movies found on this page.")
        return go_to_main_menu()

    max_title_length = max(len(movie[0]) for movie in movies_actors)

    print(f"Page {page} of {total_pages}\n")
    print(f"Showing movies and actors {offset + 1}-{min(offset + page_size, total_movies)} "
          f"of {total_movies}\n")

    for idx, (movie_title, actors) in enumerate(movies_actors, start=offset + 1):
        padding = ' ' * (max_title_length - len(movie_title) + 4 - len(str(idx)))
        print(f"{idx}. Movie: \"{movie_title}\"{padding}Actors: {actors}")

    if page < total_pages:
        print(f"Type 'next / +1' to go to the next page.")
    if page > 1:
        print(f"Type 'prev / -1' to go to the previous page.")
    print("Type 'exit' / 'q' to quit.")

    user_input = input("Your choice: ").strip().lower()

    if user_input in ['next', '+1'] and page < total_pages:
        show_movies_with_actors_with_pagination(db, page + 1, page_size)
    elif user_input in ['prev', '-1'] and page > 1:
        show_movies_with_actors_with_pagination(db, page - 1, page_size)
    elif user_input in ['exit', 'q']:
        return go_to_main_menu()
    else:
        print("Invalid input. Please try again.")
        show_movies_with_actors_with_pagination(db, page, page_size)


def get_unique_genres(db: DBClass) -> list:
    """
    Retrieves all unique movie genres from the database.

    Args:
        db: Database (sqlite3.Cursor): The db: Database object for executing SQL queries.

    Returns:
        list: A list of unique movie genres.
    """
    query = """
                SELECT DISTINCT genre 
                FROM movies 
                ORDER BY genre
            """
    return db.execute_query(query)


def show_genres(db: DBClass, selection: str = 'off') -> str | None:
    """
    Displays a list of all unique movie genres with pagination (15 genres per page)
    and allows the user to navigate through the pages.

    Args:
        db: Database (sqlite3.Cursor): The db: Database object for executing SQL queries.

    Returns:
        str | None:
            - str if user selects a genre
            - None if the user exits
    """
    genres_list = [genre[0] for genre in get_unique_genres(db)]

    result = choose_page_action(
        current_page=1,
        items=genres_list,
        item_name="genre",
        selection=selection
    )

    if result in ['exit', 'q']:
        return go_to_main_menu()
    else:
        return result


def show_movie_count_by_genre(db: DBClass) -> None:
    """
    Displays the number of movies for each genre.

    Args:
        db: Database (sqlite3.Cursor): The db: Database object for executing SQL queries.
    """
    genres = [genre[0] for genre in get_unique_genres(db)]

    print("\nMovie count by genre:")
    for genre in genres:
        # Get the count of movies for each genre
        db.cursor.execute("SELECT COUNT(*) FROM movies WHERE genre = ?", (genre,))
        movie_count = db.cursor.fetchone()[0]

        print(f"Genre: {genre} - {movie_count} movies")
    while True:
        input("\nType something to join the main menu.")
        return None


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


def show_movies_with_age(db: DBClass) -> None:
    """
    Displays all movies with their respective ages (years since release).

    Args:
        db: Database (sqlite3.Cursor): The db: Database object for executing SQL queries.
    """
    register_functions(db.connection)
    db.cursor.execute("SELECT title, release_year, movie_age(release_year) FROM movies")
    movies = db.cursor.fetchall()

    print("Movies and their age:")
    for i, (movie_title, release_year, age) in enumerate(movies, 1):
        print(f"{i}. Movie: \"{movie_title}\" — {age} years")
    while True:
        input("\nType something to join the main menu.")
        return None


def search_genre_by_part_name(db: DBClass, selection: str = 'off') -> str | None:
    """
    Prompts the user to enter a part of a genre name and returns the genre that matches the search.

    If no results are found, asks the user if they want to see all genres.

    Args:
        db: Database (sqlite3.Cursor): The db: Database object for executing SQL queries.

    Returns:
        str: The genre selected by the user, or None if not found.
    """
    attempts = 0
    while attempts < 3:
        genre_part = input("Enter part of the genre name to search for "
                           "(or 'exit'/'q' to return to the main menu): ").strip()

        if genre_part in ['exit', 'q']:
            return go_to_main_menu()

        db.connection.create_collation("CI", case_insensitive_collation)
        query = """
                    SELECT DISTINCT genre
                    FROM movies
                    WHERE genre LIKE ? COLLATE CI
                """
        genres_list: list = [genre[0] for genre in db.execute_query(query, (f"%{genre_part}%",))]

        if genres_list:
            result = choose_page_action(
                current_page=1,
                items=genres_list,
                item_name="genre",
                selection=selection
            )
            if result in ['exit', 'q']:
                return go_to_main_menu()
            else:
                return result

        else:
            print("No genres found with that name.")
            retry_choice = input(
                "What would you like to do next? Choose an option:\n"
                "1. Search again for a genre\n"
                "2. Show all genres\n"
                "3. Exit to the main menu\n"
                "Please enter the option number (1-3): ").strip()

            if retry_choice == '1':
                print("Let's try searching again...")
                return search_genre_by_part_name(db, selection)
            elif retry_choice == '2':
                if selection == 'off':
                    return str(show_genres(db))
                else:
                    return str(show_genres(db, selection))
            elif retry_choice == '3' or retry_choice in ['exit', 'q']:
                return go_to_main_menu()
            else:
                print("Invalid choice, please try again.")
                attempts += 1

    print("Too many invalid attempts. Exiting...")
    return go_to_main_menu()


def average_birth_year_of_actors_in_genre(db: DBClass) -> float | None:
    """
    Displays the average birth year of actors in movies of a specific genre.

    Args:
        db: Database (sqlite3.Cursor): The db: Database object for executing SQL queries.

    Returns:
        float: The average birth year of actors.
    """
    genre = search_genre_by_part_name(db, selection='on')
    query = """
        SELECT AVG(a.birth_year)
        FROM actors a
        JOIN movie_cast mc ON a.id = mc.actor_id
        JOIN movies m ON mc.movie_id = m.id
        WHERE m.genre = ?
    """
    average_birth_year = db.execute_query(query, (genre,))[0]

    if not average_birth_year:
        print(f"No actors found for genre: {genre}")
        return None
    print(f"Average birth year of actors in movies of genre '{genre}' is {average_birth_year:.0f}")
    return average_birth_year


def fetch_actors_and_movies(db: DBClass, results_per_page: int = 10) -> None:
    """
    Fetches and displays names of all actors and movie titles in a paginated format using UNION.

    Args:
        db (DBClass): The database object to execute queries.
        results_per_page (int): Number of results to show per page.
    """
    query = """
        SELECT name AS result, birth_year AS year FROM actors
        UNION
        SELECT title AS result, release_year AS year FROM movies
        ORDER BY year, result;
    """
    raw_results = db.execute_query(query)
    results = [f"{row[0]} ({row[1]})" for row in raw_results]
    choose_page_action(
        current_page=1,
        items=results,
        item_name="actors and movie",
        selection='off'
    )
    return go_to_main_menu()


def add_reference(db: DBClass, item1: str, item2: str, item_id: int | None,
                  func1: Callable[[DBClass, str], list],
                  func2: Callable[[], None],
                  insert_func: Callable[[Any], None]) -> None:
    """
    Prompts the user to add a reference between two items in the database.

    Args:
        db (DBClass): The database object.
        item1 (str): The name of the first item to add reference (e.g., "actor").
        item2 (str): The name of the second item to add reference (e.g., "movie").
        func1 (Callable[[DBClass, str], list]): Function to search for the first item in the database.
        func2 (Callable[[DBClass, str], None]): Function to add a new item if it does not exist.
        insert_func (Callable[[int, int], None]): Function to insert the reference between the two items.

    Returns:
        None
    """
    add_ref = input(f"Would you like to add a {item1} reference to this {item2}? "
                    f"[yes, y, 1] or go back to the main menu [no, n]: ").strip().lower()

    if add_ref not in ["yes", "y", "1"]:
        return go_to_main_menu()

    item_part = input(f"Please enter the part of the {item1} to search in database: ")
    search_results = func1(db, item_part)

    if search_results:
        search_item1 = [item[0] for item in search_results]

        if len(search_item1) > 1:
            selection = choose_page_action(
                items=search_item1,
                item_name=f"found {item1}",
                selection='on'
            )
            if selection == "exit":
                return go_to_main_menu()
            search_item1 = selection
        else:
            search_item1 = search_item1[0]
    else:
        add_new_item1 = input(
            f"There is no such {item1} in the database, would you like to add a {item1}? [yes, y, 1]: ").strip().lower()
        if add_new_item1 in ["yes", "y", "1"]:
            func2()
            search_results = func1(db, item_part)
            if not search_results:
                print(f"Failed to add {item1}.")
                return go_to_main_menu()
            search_item1 = search_results[0]
        else:
            print(f"{item1.capitalize()} was not added. {item2.capitalize()} remains unlinked.")
            return go_to_main_menu()
    get_id_func = getattr(DBClass, f"get_{item1}_id", None)
    if get_id_func:
        item1_id = get_id_func(search_item1)

        if item1_id:
            moviecast_list = [MovieCast(item1_id, item_id)]  # Додаємо до списку

            insert_func(moviecast_list)

            print(f"Reference between {item1} and {item2} added successfully.")

    return go_to_main_menu()


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
    with DBClass('kinodb.db') as db:
        options = {
            "1": insert_movie,
            "2": insert_actor,
            "3": search_movie_interactive,
            "4": show_movies_with_actors_with_pagination,
            "5": show_genres,
            "6": show_movie_count_by_genre,
            "7": show_movies_with_age,
            "8": search_genre_by_part_name,
            "9": average_birth_year_of_actors_in_genre,
            "10": fetch_actors_and_movies,
            "0": lambda: sys.exit(1)
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
                if choice == "9":
                    genre = search_genre_by_part_name(db)
                    options[choice](db, genre)
                else:
                    options[choice](db)
            else:
                print("Invalid choice. Try again.")

            if choice == "0":
                print("Finishing work with database..."
                      "Thank you, have a nice to meet!")
                sys.exit(1)


if __name__ == "__main__":
    main()
