"""
IStorage interface defines methods for movie storage operations.

Methods:
- _list_movies() -> dict[str, dict]: Returns a dictionary of movies with ratings and years.
- _add_movie(title: str, year: int, rating: float, poster: str) -> None: Adds a movie to the database.
- _delete_movie(title: str) -> None: Deletes a movie from the database.
"""

from abc import ABC, abstractmethod

# Movie dictionary keys
TITLE = "Title"
YEAR = "Year"
RATING = "Rating"
POSTER = "Poster"


class IStorage(ABC):
    @abstractmethod
    def _list_movies(self) -> dict[str, dict]:
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.
        The function loads the information from the JSON
        file and returns the data.
        For example, the function may return:
        {
            "Titanic":
                {"rating": 9, "year": 1999},
            "Pulp Fiction":
                {"rating": 10, "year": 1999},
            ...
        }
        """
        pass

    @abstractmethod
    def _add_movie(self, title, year, rating, poster, imdb_id) -> None:
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        pass

    @abstractmethod
    def _delete_movie(self, title) -> None:
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        pass
