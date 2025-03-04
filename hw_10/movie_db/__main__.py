"""
This is the main module for interacting with the "Kinodb database".

Usage:
    To set up the database, run this file:
    python -m movie_db.database.database_setup
    To interact with the database, run this file:
    python -m movie_db.__main__
    You should run this code at one level higher than the movie_db folder.
"""
from .ui.movie_database import main

if __name__ == "__main__":
    main()
