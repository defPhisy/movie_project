"""
Main entry point for launching the MovieApp.

Initializes storage, sets up the MovieApp with CSV- or JSON-based movie data,
and runs the application. To switch to JSON storage, modify the storage
initialization and uncomment the relevant import.

Usage:
    Run this script to start the MovieApp with current storage settings.
"""

import os
from arg_handling import args
from movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson


def main() -> None:
    STORAGE_PATH = "data"

    # default db name
    db_name = "movie_db"
    # default file extension
    ext = ".json"

    if args.name:
        db_name = args.name

    # default storage is json
    db_path = get_file_path(STORAGE_PATH, db_name, ext)

    if args.csv:
        ext = ".csv"
        db_path = get_file_path(STORAGE_PATH, db_name, ext)
        storage = StorageCsv(db_path)
    else:
        storage = StorageJson(db_path)

    movie_app = MovieApp(storage)
    movie_app.run()


def get_file_path(storage_path, name, extension):
    db_file = name + extension
    return os.path.join(storage_path, db_file)


if __name__ == "__main__":
    main()
