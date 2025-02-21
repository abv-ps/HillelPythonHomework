"""
This module defines data classes for representing entities in a movie database system.

Classes:
- Movie: Represents a movie entity with a title, release year, and genre.
- Actor: Represents an actor entity with a name and birth year.
- MovieCast: Represents a relationship between a movie and an actor,
associating movie IDs with actor IDs.

These classes are used to structure and store data for movies, actors,
and their relationships in the database.
"""

from dataclasses import dataclass


@dataclass
class Movie:
    """
    Represents a movie entity.
    """
    title: str
    release_year: int
    genre: str | None


@dataclass
class Actor:
    """
    Represents an actor entity.
    """
    name: str
    birth_year: int


@dataclass
class MovieCast:
    """
    Represents a relationship between a movie and an actor.
    """
    movie_id: int
    actor_id: int
