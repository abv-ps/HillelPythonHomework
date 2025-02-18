import sqlite3
import datetime
from typing import Optional


def connect_db(db_name: str) -> sqlite3.Connection:
    return sqlite3.connect(db_name)


def choose_page_action(current_page: int, total_pages: int, movies: list) -> int:
    """
    Prompts the user to choose a movie or navigate between pages (next, prev).

    Args:
        current_page (int): The current page number.
        total_pages (int): The total number of pages.
        movies (list): The list of movies to select from.

    Returns:
        int: The new current page number, or -1 if user selected a movie.
    """
    while True:
        movie_choice = input(
            f"Select a movie (1-{len(movies)}) or type 'next'|'+1' to go to the next page, "
            f"type 'prev'|'-1' to go to the previous page: ").strip().lower()

        if movie_choice.isdigit() and 1 <= int(movie_choice) <= len(movies):
            return -1  # Indicating the user selected a movie
        elif movie_choice in ['next', '+1'] and current_page < total_pages:
            return current_page + 1  # Go to the next page
        elif movie_choice in ['prev', '-1'] and current_page > 1:
            return current_page - 1  # Go to the previous page
        else:
            print("Invalid selection or you are already at the first/last page. Please try again.")


def search_movie_by_keyword(cursor: sqlite3.Cursor) -> Optional[str]:
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
        cursor.execute("SELECT COUNT(*) FROM movies WHERE title LIKE ?", (f"%{movie_name}%",))
        count_of_founded_movies: int = int(cursor.fetchone()[0])

        if count_of_founded_movies == 0:
            print("No movies found with that title.")
            attempts += 1
        else:
            total_pages: int = (count_of_founded_movies // results_per_page) + (
                1 if count_of_founded_movies % results_per_page > 0 else 0)
            current_page: int = 1
            while current_page <= total_pages:
                offset = (current_page - 1) * results_per_page
                cursor.execute("SELECT title FROM movies WHERE title LIKE ? ORDER BY title LIMIT ? OFFSET ?",
                               (f"%{movie_name}%", results_per_page, offset))
                movies: list = cursor.fetchall()
                print(f"\nPage {current_page} of {total_pages}:")
                for i, (m_title,) in enumerate(movies, 1):
                    print(f"{(current_page - 1) * results_per_page + i}. {m_title}")

                # Using the choose_page_action function for navigation
                new_page = choose_page_action(current_page, total_pages, movies)

                if new_page == -1:
                    # If -1 is returned, it means the user selected a movie
                    movie_choice = int(input(f"Select a movie (1-{len(movies)}): ").strip())
                    movie_title = movies[movie_choice - 1][0]
                    return movie_title
                else:
                    current_page = new_page
    print("Too many invalid attempts. Exiting...")
    return None


def insert_movie(cursor: sqlite3.Cursor) -> None:
    title = search_movie_by_keyword(cursor)
    if title:
        print(f"Using existing movie '{title}'.")
        return

    title = input("Enter the movie title: ")
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
    cursor.execute('''INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)''',
                   (title, release_year, genre))
    cursor.connection.commit()
    print(f"Movie '{title}' added.")


def insert_actor(cursor: sqlite3.Cursor) -> None:
    actor_name = input("Enter the actor's name: ")
    movie_title = search_movie_by_keyword(cursor)
    if not movie_title:
        print("No valid movie found. Exiting...")
        return

    cursor.execute("SELECT id FROM actors WHERE name = ?", (actor_name,))
    existing_actor = cursor.fetchone()
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

        cursor.execute("INSERT INTO actors (name, birth_year) VALUES (?, ?)", (actor_name, birth_year))
        actor_id = cursor.lastrowid
        cursor.connection.commit()
        print(f"Actor '{actor_name}' added.")
    else:
        actor_id = existing_actor[0]

    cursor.execute("SELECT id FROM movies WHERE title = ?", (movie_title,))
    movie_id = cursor.fetchone()[0]
    cursor.execute("SELECT 1 FROM movie_cast WHERE movie_id = ? AND actor_id = ?", (movie_id, actor_id))
    if cursor.fetchone():
        print(f"Actor '{actor_name}' is already associated with '{movie_title}'.")
    else:
        cursor.execute("INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)", (movie_id, actor_id))
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

    while True:
        # Calculate the OFFSET for pagination
        offset = (current_page - 1) * page_size

        # SQL query to get movies with their actors
        cursor.execute('''
            SELECT m.title, GROUP_CONCAT(a.name, ', ') AS actors
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

        print(f"Movies and Actors - Page {current_page}:\n")

        for i, (movie_title, actors) in enumerate(movies_actors, 1):
            print(f"{(current_page - 1) * page_size + i}. Фільм: \"{movie_title}\", Актори: {actors}")

        # Call the function to handle page navigation
        new_page = choose_page_action(current_page, (len(movies_actors) // page_size) + 1, movies_actors)

        if new_page == -1:
            # If -1 is returned, it means a movie was selected, so handle it
            movie_choice = int(input(f"Select a movie (1-{len(movies_actors)}): ").strip())
            movie_title = movies_actors[movie_choice - 1][0]
            print(f"You selected the movie: {movie_title}")
            break
        else:
            current_page = new_page


def get_unique_genres(cursor: sqlite3.Cursor) -> list:
    """
    Retrieves all unique movie genres from the database.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.

    Returns:
        list: A list of unique movie genres.
    """
    cursor.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
    genres = cursor.fetchall()
    return [genre[0] for genre in genres]

def show_genres(cursor: sqlite3.Cursor) -> None:
    """
    Displays a list of all unique movie genres with pagination (15 genres per page)
    and allows the user to navigate through the pages.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
    """
    genres = get_unique_genres(cursor)
    results_per_page = 15

    if not genres:
        print("No genres found.")
        return

    total_pages = (len(genres) // results_per_page) + (1 if len(genres) % results_per_page > 0 else 0)
    current_page = 1

    while current_page <= total_pages:
        offset = (current_page - 1) * results_per_page
        page_genres = genres[offset:offset + results_per_page]

        print(f"Page {current_page} of {total_pages}:\n")
        for i, (genre,) in enumerate(page_genres, 1):
            print(f"{(current_page - 1) * results_per_page + i}. {genre}")

        # Ask user to navigate pages using the choose_page_action function
        new_page = choose_page_action(current_page, total_pages, page_genres)

        if new_page == -1:
            genre_choice = int(input(f"Select a genre (1-{len(page_genres)}): ").strip())
            selected_genre = page_genres[genre_choice - 1][0]
            print(f"You selected the genre: {selected_genre}")
            break
        else:
            current_page = new_page


def show_movie_count_by_genre(cursor: sqlite3.Cursor) -> None:
    """
    Displays the number of movies for each genre using the get_unique_genres function,
    and allows the user to select a genre and see how many movies belong to it.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
    """
    genres = get_unique_genres(cursor)

    if not genres:
        print("No genres found.")
        return

    print("\nGenres available:")
    for i, (genre,) in enumerate(genres, 1):
        print(f"{i}. {genre}")

    # Ask the user to select a genre
    genre_choice = int(input(f"Select a genre (1-{len(genres)}): ").strip())
    selected_genre = genres[genre_choice - 1][0]

    # Get the count of movies for the selected genre
    cursor.execute("SELECT COUNT(*) FROM movies WHERE genre = ?", (selected_genre,))
    movie_count = cursor.fetchone()[0]

    print(f"\nThere are {movie_count} movies in the genre '{selected_genre}'.")

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

def show_movies_with_age(cursor: sqlite3.Cursor) -> None:
    """
    Displays all movies with their respective ages (years since release).

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
    """
    cursor.execute("SELECT title, release_year FROM movies")
    movies = cursor.fetchall()

    if not movies:
        print("No movies found.")
        return

    print("Movies and their age:")
    for i, (movie_title, release_year) in enumerate(movies, 1):
        age = movie_age(release_year)  # Calculate movie age
        print(f"{i}. Movie: \"{movie_title}\" — {age} years")


def search_genre_by_part_name(cursor: sqlite3.Cursor) -> str|None:
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
        genre_part = input("Enter part of the genre name to search for: ").strip()

        # Fetch genres that match the entered part of the genre name
        cursor.execute("SELECT DISTINCT genre FROM movies WHERE genre LIKE ?", (f"%{genre_part}%",))
        genres = cursor.fetchall()

        if genres:
            print(f"Found genres: {[genre[0] for genre in genres]}")
            genre_choice = input("Select a genre from the above list: ").strip()
            if genre_choice in [genre[0] for genre in genres]:
                return genre_choice
            else:
                print("Invalid genre selection. Try again.")
                attempts += 1
        else:
            print("No genres found with that name.")
            retry_choice = input("Would you like to see all genres? [yes, y, 1] or [no, n, 0]: ").strip().lower()
            if retry_choice in ['yes', 'y', '1']:
                return show_genres(cursor)
            else:
                print("You can try again.")
                attempts += 1

    print("Too many invalid attempts. Exiting...")
    return None


def average_birth_year_of_actors_in_genre(cursor: sqlite3.Cursor, genre: str) -> float|None:
    """
    Displays the average birth year of actors in movies of a specific genre.

    Args:
        cursor (sqlite3.Cursor): The cursor object for executing SQL queries.
        genre (str): The genre of the movies to filter by.

    Returns:
        float: The average birth year of actors.
    """
    cursor.execute("""
        SELECT a.birth_year
        FROM actors a
        JOIN movie_cast mc ON a.id = mc.actor_id
        JOIN movies m ON mc.movie_id = m.id
        WHERE m.genre = ?
    """, (genre,))
    birth_years = cursor.fetchall()

    if not birth_years:
        print(f"No actors found for genre: {genre}")
        return

    total_birth_years = sum(year[0] for year in birth_years)
    average_birth_year = total_birth_years / len(birth_years)

    print(f"Average birth year of actors in movies of genre '{genre}': {average_birth_year:.0f}")
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

    results = cursor.fetchall()
    total_results = len(results)
    total_pages = (total_results // results_per_page) + (1 if total_results % results_per_page > 0 else 0)
    current_page = 1

    while True:
        start_index = (current_page - 1) * results_per_page
        end_index = start_index + results_per_page
        page_results = results[start_index:end_index]

        print(f"\nPage {current_page}/{total_pages}")
        for i, (result,) in enumerate(page_results, 1):
            print(f"{i}. {result}")

        action = choose_page_action(current_page, total_pages, page_results)
        if action == -1:
            return
        else:
            current_page = action


def main():
    conn = connect_db("movies.db")
    cursor = conn.cursor()
    while True:
        print("\n1. Add Movie\n2. Add Actor\n3. Search Movie by keyword"
              "\n4. Show all movies with actors\n5. Show all genres"
              "\n6. Show movie count by genre\n7. Show movies with age"
              "\n8. Search genre by part name\n9. Show average birth year of actors in genre"
              "\10. Show names of all actors and titles of all movies\n0. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            insert_movie(cursor)
        elif choice == "2":
            insert_actor(cursor)
        elif choice == "3":
            search_movie_by_keyword(cursor)
        elif choice == "4":
            show_movies_with_actors(cursor)
        elif choice == "5":
            show_genres(cursor)
        elif choice == "6":
            show_movie_count_by_genre(cursor)
        elif choice == "7":
            show_movies_with_age(cursor)
        elif choice == "8":
            search_genre_by_part_name(cursor)
        elif choice == "9":
            average_birth_year_of_actors_in_genre(cursor, search_genre_by_part_name(cursor))
        elif choice == "10":
            fetch_actors_and_movies(cursor)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")
    conn.close()


if __name__ == "__main__":
    main()
