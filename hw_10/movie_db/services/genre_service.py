"""
Module providing genre-related services, including retrieving, searching,
and displaying movie genres with pagination.
"""

from typing import List, Optional

from ..database.database_setup import Database as DBClass
from ..database.db_models import DatabaseHandler as DBHandler
from ..utils.helpers import (
    choose_page_action,
    handle_no_items_found
)


class GenreService:
    """
    A service class for managing movie genres, including retrieval, searching,
    and displaying genres with pagination.
    """

    @staticmethod
    def get_unique_genres(db: DBClass) -> List[str]:
        """
        Retrieves all unique movie genres from the database.

        Args:
            db (DBClass): The database object used to execute SQL queries.

        Returns:
            List[str]: A list of unique movie genres, sorted alphabetically.
        """
        query = """
            SELECT DISTINCT genre 
            FROM movies 
            ORDER BY genre
        """
        return [genre[0] for genre in db.execute_query(query)]

    @staticmethod
    def show_genres(db: DBClass, selection: str = 'off') -> Optional[str]:
        """
        Displays a list of all unique movie genres with pagination and allows selection.

        Args:
            db (DBClass): The database object used to execute SQL queries.
            selection (str, optional): Determines how items are displayed. Defaults to 'off'.

        Returns:
            Optional[str]: The selected genre name or None if the user exits.
        """
        genres_list = GenreService.get_unique_genres(db)
        result = choose_page_action(
            current_page=1,
            items=genres_list,
            item_name="genre",
            selection=selection
        )
        return None if result in ['exit', 'q'] else result

    @staticmethod
    def search_genre_by_part_name(db: DBClass, selection: str = 'off') -> Optional[str]:
        """
        Prompts the user to enter part of a genre name and returns a matching genre.

        Args:
            db (DBClass): The database object used to execute SQL queries.
            selection (str, optional): Determines how items are displayed. Defaults to 'off'.

        Returns:
            Optional[str]: The selected genre name or None if no valid genre is found.
        """
        genre_part = input(
            "Enter part of the genre name to search for (or 'exit'/'q' to return to the main menu): ").strip()
        if genre_part in ['exit', 'q']:
            from ..ui.movie_database import go_to_main_menu
            return go_to_main_menu("According to your choice 'exit'")

        db.connection.create_collation("CI", DBHandler.case_insensitive_collation)
        query = """
            SELECT DISTINCT genre
            FROM movies
            WHERE genre LIKE ? COLLATE CI
        """
        genres_list = [genre[0] for genre in db.execute_query(query, (f"%{genre_part}%",))]

        if genres_list:
            result = choose_page_action(
                current_page=1,
                items=genres_list,
                item_name="genre",
                selection=selection
            )
            print(f"You select the {result}")
            from ..ui.movie_database import go_to_main_menu
            return go_to_main_menu("According to your choice 'exit'") if result in ['exit', 'q'] else result

        return handle_no_items_found(
            item_name="genre",
            items_func=lambda: GenreService.show_genres(db, selection),
            retry_func=lambda: GenreService.search_genre_by_part_name(db, selection)
        )

