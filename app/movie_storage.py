import json

FILENAME_DB = "data/movie_db.json"

# Movie dictionary keys
TITLE = "Title"
YEAR = "Year"
RATING = "Rating"


def get_movie_data() -> list[dict]:
    with open(FILENAME_DB, "r") as fileobj:
        data = json.loads(fileobj.read())
    return data


def list_movies() -> dict[str, dict]:
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    movies = get_movie_data()
    movie_dict = {}
    for movie in movies:
        movie_dict[movie[TITLE]] = {
            "rating": movie["Rating"],
            "year": movie["Year"],
        }
    return movie_dict


def add_movie(title, year, rating) -> None:
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movie_data()
    movies.append({"Title": title, "Rating": rating, "Year": year})

    save_movies(movies)


def delete_movie(title) -> None:
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movie_data()
    for index, movie in enumerate(movies):
        if movie[TITLE].lower() == title.lower():
            movies.remove(movies[index])

    save_movies(movies)


def update_movie(title, rating) -> None:
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movie_data()
    for index, movie in enumerate(movies):
        if movie[TITLE].lower() == title.lower():
            movies[index]["Rating"] = rating

    save_movies(movies)


def save_movies(movies) -> None:
    """Save movies in json file.

    Arguments:
        movies -- dictionary of all movies
    """
    with open(FILENAME_DB, "w") as fileobj:
        fileobj.write(json.dumps(movies))
