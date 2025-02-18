from dataclasses import dataclass
from typing import Optional

@dataclass
class Movie:
    """
    Represents a movie entity.
    """
    id: Optional[int]
    title: str
    release_year: int
    genre: str

@dataclass
class Actor:
    """
    Represents an actor entity.
    """
    id: Optional[int]
    name: str
    birth_year: int

@dataclass
class MovieCast:
    """
    Represents a relationship between a movie and an actor.
    """
    movie_id: int
    actor_id: int
