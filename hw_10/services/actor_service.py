"""
This module provides the `ActorService` class, which manages actor-related operations
within the database.

Classes:
- ActorService: A service class responsible for handling actor-related database operations,
  such as searching for actors by keyword and inserting new actors.
"""

from typing import Optional

from ..database.database_setup import Database as DBClass
from ..database.db_models import Actor, DatabaseHandler as DBHandler
from ..utils.validators import Validator


class ActorService:
    """
    A service class for managing actor-related database operations.
    """

    @staticmethod
    def find_actors_by_keyword(db: DBClass, keyword: str) -> list[tuple[str, int]]:
        """
        Searches for actors by keyword without user interaction.

        Args:
            db (DBClass): The database object for executing SQL queries.
            keyword (str): The keyword to search for in actor names.

        Returns:
            list[tuple[str, int]]: A list of tuples containing actor names and birth years.
        """
        result = DBHandler.find_by_keyword(
            connection=db.connection,
            table="actors",
            keyword=keyword,
            columns=["name", "birth_year"],
            order_by="name"
        )

        return list(set((actor[0], actor[1]) for actor in result)) if result else []

    @staticmethod
    def insert_actor(db: DBClass, movie_name: Optional[str] = None) -> None:
        """
        Inserts a new actor into the database and associates them with movies.

        Args:
            db (DBClass): The SQLite database class used for database interactions.
            movie_name (Optional[str]): The name of the movie to associate the actor with (optional).
                If no movie is provided, the actor will be added without association.

        Returns:
            None: This function does not return a value. It interacts directly with the database.
        """
        actor_name = input("Enter the actor's name: ")
        v = Validator()
        actor_name_sub = v.validate_actor_name_genre(actor_name, "actor's name")

        if not actor_name_sub[0]:
            from ..ui.movie_database import go_to_main_menu
            return go_to_main_menu()

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
        from .movie_service import MovieService
        from ..ui.movie_database import add_reference
        add_reference(
            db=db,
            item1='movie',
            item2='actor',
            item_id=actor_id,
            func1=lambda db, keyword: MovieService.find_movies_by_keyword(db, keyword),
            func2=lambda: MovieService.insert_movie(db, movie_name),
            insert_func=lambda movie_cast: db.insert_movie_cast(movie_cast)
        )
