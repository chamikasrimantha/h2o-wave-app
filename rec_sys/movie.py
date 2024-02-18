from dataclasses import dataclass


@dataclass
class Movie:
    title: str
    director: str
    release_year: int
    genre: str
    rating: float
    poster: str
