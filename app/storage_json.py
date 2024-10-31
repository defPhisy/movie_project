import json

from istorage import RATING, TITLE, YEAR, IStorage


class StorageJson(IStorage):
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def get_movie_data(self) -> list[dict]:
        with open(self.file_path, "r") as file:
            data = json.loads(file.read())
        return data

    def _list_movies(self) -> dict[str, dict]:
        movies = self.get_movie_data()
        movie_dict = {}
        for movie in movies:
            movie_dict[movie[TITLE]] = {
                "rating": movie[RATING],
                "year": movie[YEAR],
            }
        return movie_dict

    def _add_movie(self, title, year, rating, poster="placeholder") -> None:
        movies = self.get_movie_data()
        movies.append({
            "Title": title,
            "Rating": rating,
            "Year": year,
            "poster": poster,
        })

        self._save_movies(movies)

    def _delete_movie(self, title):
        movies = self.get_movie_data()
        for index, movie in enumerate(movies):
            if movie[TITLE].lower() == title.lower():
                movies.remove(movies[index])

        self._save_movies(movies)

    def _save_movies(self, movies) -> None:
        """Save movies in json file.

        Arguments:
            movies -- dictionary of all movies
        """
        with open(self.file_path, "w") as fileobj:
            fileobj.write(json.dumps(movies))
