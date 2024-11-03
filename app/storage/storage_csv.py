"""
StorageCsv manages movie data in a CSV file, implementing the IStorage interface.

Methods:
- get_movie_data() -> list[dict]: Loads movie records.
- _list_movies() -> dict[str, dict]: Retrieves movies with ratings and years.
- _add_movie(title: str, year: int, rating: float, poster: str = "placeholder") -> None: Adds a movie.
- _delete_movie(title: str) -> None: Deletes a movie by title.
- _save_movies(movies: list[dict]) -> None: Saves movies to the JSON file.
"""

import csv
import os

from storage.istorage import RATING, TITLE, YEAR, POSTER, IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path) -> None:
        self.file_path = file_path

        if not os.path.exists(file_path):
            self.create_new_file()

    def create_new_file(self):
        with open(self.file_path, "w") as file:
            file.write("Title,Rating,Year,Poster")

    def get_movie_data(self) -> list[dict]:
        with open(self.file_path, "r") as file:
            return [
                {
                    "Title": row["Title"],
                    "Rating": float(row["Rating"]),
                    "Year": int(row["Year"]),
                    "Poster": row["Poster"],
                    "ID": row["ID"],
                }
                for row in csv.DictReader(file)
            ]

    def _list_movies(self) -> dict[str, dict]:
        movies = self.get_movie_data()
        movie_dict = {}
        if movies:
            for movie in movies:
                movie_dict[movie[TITLE]] = {
                    "rating": movie[RATING],
                    "year": movie[YEAR],
                    "poster": movie[POSTER],
                }
        return movie_dict

    def _add_movie(self, title, year, rating, poster, imdb_id) -> None:
        movies = self.get_movie_data()
        movies.append({
            "Title": title,
            "Rating": float(rating),
            "Year": int(year),
            "Poster": poster,
            "ID": imdb_id,
        })

        self._save_movies(movies)

    def _delete_movie(self, title: str) -> None:
        movies = self.get_movie_data()
        new_movies = [
            movie for movie in movies if movie[TITLE].lower() != title.lower()
        ]

        self._save_movies(new_movies)

    def _save_movies(self, movies) -> None:
        """Save movies in json file.

        Arguments:
            movies -- dictionary of all movies
        """

        field_names = ["Title", "Rating", "Year", "Poster"]

        with open(self.file_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            if movies:
                writer.writerows(movies)
