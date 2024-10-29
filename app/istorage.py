from abc import ABC, abstractmethod
import json

# Movie dictionary keys
TITLE = "Title"
YEAR = "Year"
RATING = "Rating"


class IStorage(ABC):
    @abstractmethod
    def _list_movies(self):
        pass

    @abstractmethod
    def _add_movie(self, title, year, rating, poster):
        pass

    @abstractmethod
    def _delete_movie(self, title):
        pass

    @abstractmethod
    def _update_movie(self, title, rating):
        pass
