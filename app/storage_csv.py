import csv

from istorage import RATING, TITLE, YEAR, IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def get_movie_data(self) -> list[dict]:
        with open(self.file_path, "r") as file:
            return [
                {
                    "Title": row["Title"],
                    "Rating": float(row["Rating"]),
                    "Year": int(row["Year"]),
                    "Poster": row["Poster"],
                }
                for row in csv.DictReader(file)
            ]

    def _list_movies(self) -> dict[str, dict]:
        movies = self.get_movie_data()
        return {
            movie[TITLE]: {"rating": movie[RATING], "year": movie[YEAR]}
            for movie in movies
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

        field_names = movies[0].keys()

        with open(self.file_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(movies)
