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
    def insert_actor(db: DBClass,
                     actor_name: Optional[str] = None,
                     movie_title: Optional[str] = None) -> None:
        """
        Inserts a new actor into the database and associates them with movies.

        Args:
            db (DBClass): The SQLite database class used for database interactions.
            movie_title (Optional[str]): The name of the movie to associate the actor with (optional).
                If no movie is provided, the actor will be added without association.

        Returns:
            None: This function does not return a value. It interacts directly with the database.
        """
        from ..ui.movie_database import go_to_main_menu

        if not actor_name:
            actor_name = input("Enter the actor's name: ")
            v = Validator()
            actor_name_sub = v.validate_actor_name_genre(actor_name, "actor's name")

            if not actor_name_sub[0]:
                return go_to_main_menu("Actor name is empty.")

            actor_name = actor_name_sub[1]

        existing_actor = db.get_actor_id(actor_name)

        if not existing_actor:
            v = Validator()
            is_valid, birth_year = v.validate_year(
                year=int(input("Enter the actor's birth year: ")),
                year_type="birth"
            )

            if not is_valid:
                return go_to_main_menu("Maximum attempts reached. Invalid input.")

            db.start_savepoint()
            db.insert_actors([Actor(actor_name, birth_year)])
            db.release_savepoint()
            actor_id = db.cursor.lastrowid
            print(f"Actor '{actor_name}' added.")
            print(f"Movie is '{movie_title}'.")
        else:
            actor_id = existing_actor

        from .movie_service import MovieService
        from ..ui.movie_database import add_reference

        if not movie_title:
            return add_reference(
                db=db,
                item1='movie',
                item2='actor',
                item_id=actor_id,
                func1=MovieService.find_movies_by_keyword
            )

