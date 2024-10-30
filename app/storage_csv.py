import csv
from istorage import IStorage
from istorage import TITLE, YEAR, RATING


class StorageCsv(IStorage):
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def get_movie_data(self) -> list[dict]:
        with open(self.file_path, "r") as file:
            dict_reader = csv.DictReader(file)
            data = list(dict_reader)
            movies = []
            for row in data:
                title = row["Title"]
                rating = float(row["Rating"])
                year = int(row["Year"])
                poster = row["Poster"]
                movies.append({
                    "Title": title,
                    "Rating": rating,
                    "Year": year,
                    "Poster": poster,
                })
        return movies

    def _list_movies(self) -> dict[str, dict]:
        movies = self.get_movie_data()
        movie_dict = {}
        for movie in movies:
            movie_dict[movie[TITLE]] = {
                "rating": movie[RATING],
                "year": movie[YEAR],
                "poster": movie["Poster"],
            }
        print(movie_dict)
        return movie_dict

    def _add_movie(self, title, year, rating, poster="placeholder") -> None:
        movies = self.get_movie_data()
        movies.append({
            "Title": title,
            "Rating": rating,
            "Year": year,
            "Poster": poster,
        })

        self._save_movies(movies)

    def _delete_movie(self, title):
        movies = self.get_movie_data()
        for index, movie in enumerate(movies):
            if movie[TITLE].lower() == title.lower():
                movies.remove(movies[index])

        self._save_movies(movies)

    def _update_movie(self, title, rating) -> None:
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

        field_names = movies[0].keys()

        with open(self.file_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(movies)
