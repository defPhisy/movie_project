import json
from istorage import IStorage
from istorage import TITLE, YEAR, RATING


class StorageJson(IStorage):
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def get_movie_data(self) -> list[dict]:
        with open(self.file_path, "r") as file:
            data = json.loads(file.read())
        return data

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

        movies = self.get_movie_data()
        movie_dict = {}
        for movie in movies:
            movie_dict[movie[TITLE]] = {
                "rating": movie[RATING],
                "year": movie[YEAR],
            }
        return movie_dict

    def _add_movie(self, title, year, rating, poster="placeholder"):
        """
        Adds a movie to the movies database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.get_movie_data()
        movies.append({
            "Title": title,
            "Rating": rating,
            "Year": year,
            "poster": poster,
        })

        self._save_movies(movies)

    def _delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.get_movie_data()
        for index, movie in enumerate(movies):
            if movie[TITLE].lower() == title.lower():
                movies.remove(movies[index])

        self._save_movies(movies)

    def _update_movie(self, title, rating):
        """
        Updates a movie from the movies database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.get_movie_data()
        for index, movie in enumerate(movies):
            if movie[TITLE].lower() == title.lower():
                movies[index]["Rating"] = rating

        self._save_movies(movies)

    def _save_movies(self, movies) -> None:
        """Save movies in json file.

        Arguments:
            movies -- dictionary of all movies
        """
        with open(self.file_path, "w") as fileobj:
            fileobj.write(json.dumps(movies))
