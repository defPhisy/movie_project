"""
Main entry point for launching the MovieApp.

Initializes storage, sets up the MovieApp with CSV- or JSON-based movie data,
and runs the application. To switch to JSON storage, modify the storage
initialization and uncomment the relevant import.

Usage:
    Run this script to start the MovieApp with current storage settings.
"""

from movie_app import MovieApp
from storage.storage_csv import StorageCsv

# from storage_json import StorageJson


def main() -> None:
    # for json storage use storage = StorageCsv(filename) and uncomment import
    storage = StorageCsv("app/data/movie_db.csv")
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
