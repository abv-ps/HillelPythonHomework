import sqlite3
from typing import Optional


def connect_db(db_name: str) -> sqlite3.Connection:
    """
    Establish a connection to the SQLite database.

    :param db_name: Name of the database file.
    :return: SQLite connection object.
    """
    return sqlite3.connect(db_name)


def insert_movie(cursor: sqlite3.Cursor) -> None:
    """
    Inserts a movie into the database and prompts to add actors to it.
    """
    title = input("Enter the movie title: ")

    # Перевіряємо, чи фільм з такою назвою вже є в базі даних
    cursor.execute('''SELECT id, title, release_year FROM movies WHERE title = ?''', (title,))
    existing_movie = cursor.fetchone()

    if existing_movie:
        print(f"The movie '{title}' already exists in the database with ID {existing_movie[0]}.")
        movie_id = existing_movie[0]  # Використовуємо існуючий movie_id
    else:
        # Якщо фільм не існує в базі, додаємо новий
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
        movie_id = cursor.lastrowid
        print(f"Movie '{title}' added with ID {movie_id}.")
        cursor.connection.commit()

    # Запит на додавання акторів до фільму
    add_actors = input("Would you like to add actors to this movie? (yes(1)/no(0)): ").lower()
    if add_actors in ['yes', '1']:  # Перевірка на 'yes' або '1'
        insert_actor(cursor, movie_id)

def insert_actor(cursor: sqlite3.Cursor, movie_id: Optional[int] = None) -> None:
    """
    Inserts an actor into the database and associates them with a movie.
    """
    actor_name = input("Enter the actor's name: ")

    try:
        actor_birth_year = int(input("Enter the actor's birth year: "))
    except ValueError:
        print("Invalid birth year. Please enter a valid number.")
        return

    # Перевірка, чи актор вже є в базі даних
    cursor.execute("SELECT id FROM actors WHERE name = ?", (actor_name,))
    existing_actor = cursor.fetchone()

    if existing_actor:
        print(f"Actor '{actor_name}' already exists in the database.")
        actor_id = existing_actor[0]
    else:
        # Якщо актора немає в базі, додаємо новий
        cursor.execute('''INSERT INTO actors (name, birth_year) VALUES (?, ?)''',
                       (actor_name, actor_birth_year))
        actor_id = cursor.lastrowid
        cursor.connection.commit()
        print(f"Actor '{actor_name}' added with ID {actor_id}.")

    # Якщо movie_id не передано, запитуємо користувача для пошуку фільму
    if not movie_id:
        movie_found = False
        attempts = 0

        while attempts < 3:
            movie_name = input("Enter a part of the movie title to search for: ")
            cursor.execute("SELECT id, title FROM movies WHERE title LIKE ? ORDER BY title",
                           (f"%{movie_name}%",))
            movies = cursor.fetchall()

            if not movies:
                print("No movies found with that title.")
                attempts += 1
                if attempts == 3:
                    print("Too many failed attempts. You can either try adding a new movie or exit.")
                    action = input("Would you like to add a new movie? (yes/no): ").lower()
                    if action in ['yes', 'y']:
                        insert_movie(cursor)  # Запускаємо функцію для додавання фільму
                    return
            else:
                print("Found the following movies:")
                for i, (m_id, m_title) in enumerate(movies, 1):
                    print(f"{i}. {m_title}")

                try:
                    movie_choice = int(input(f"Select a movie (1-{len(movies)}): "))
                    movie_id = movies[movie_choice - 1][0]
                    movie_found = True
                    break
                except (ValueError, IndexError):
                    print("Invalid selection. Please select a valid number.")
                    attempts += 1

        if not movie_found:
            print("No movie selected or found. Exiting...")
            return

    # Перевірка, чи вже існує зв'язок між актором та фільмом у таблиці movie_cast
    cursor.execute('''SELECT 1 FROM movie_cast WHERE movie_id = ? AND actor_id = ?''',
                   (movie_id, actor_id))
    existing_cast = cursor.fetchone()

    if existing_cast:
        print(f"Actor '{actor_name}' is already associated with the movie '{movie_id}'.")
    else:
        # Якщо зв'язок відсутній, додаємо його
        cursor.execute('''INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)''',
                       (movie_id, actor_id))
        cursor.connection.commit()
        print(f"Actor '{actor_name}' added and associated with movie ID {movie_id}.")


        print("Found the following movies:")
        for i, (m_id, m_title) in enumerate(movies, 1):
            print(f"{i}. {m_title}")

        try:
            movie_choice = int(input(f"Select a movie (1-{len(movies)}): "))
            movie_id = movies[movie_choice - 1][0]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

    cursor.execute('''INSERT INTO actors (name, birth_year) VALUES (?, ?)''',
                   (actor_name, actor_birth_year))
    actor_id = cursor.lastrowid
    cursor.connection.commit()

    cursor.execute('''INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)''',
                   (movie_id, actor_id))
    cursor.connection.commit()

    print(f"Actor '{actor_name}' added and associated with movie ID {movie_id}.")


def main():
    conn = connect_db("movies.db")
    cursor = conn.cursor()

    while True:
        print("\n1. Add Movie\n2. Add Actor\n3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            insert_movie(cursor)
        elif choice == "2":
            insert_actor(cursor)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please select again.")

    conn.close()


if __name__ == "__main__":
    main()
