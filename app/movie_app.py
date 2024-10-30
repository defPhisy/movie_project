import datetime
import random
import statistics
import os

from colorama import Fore, Style
from istorage import RATING, TITLE, YEAR
from thefuzz import process
from movie_api import request_for_movie


class MovieApp:
    def __init__(self, storage) -> None:
        self.storage = storage
        self.movies = self.storage.get_movie_data()

    # 0 Exit
    def _print_bye(self) -> None:
        """Print 'Good Bye' before program exits"""
        print("")
        self._print_color("Good Bye", "blue")
        print("")

    # 1 List movies
    def _print_movie_list(self) -> None:
        """Print all movies in database."""
        self.movies = self.storage.get_movie_data()
        print("")
        print(len(self.movies), "movies in total")
        for movie in self.movies:
            print(f"{movie[TITLE]} ({movie[YEAR]}): {movie[RATING]} {movie["Poster"]}")

        self._enter_to_continue()

    # 2 Add movie
    def _prompt_user_to_add_movie(self) -> None:
        """Prompt user to add movie,
        checks if it exists and adds movie to database.
        It re-prompts for a movie if user decides to add another movie.
        """
        print("")
        movie_title = self._get_valid_movie_title_from_user(
            case_sensitive=False, reverse=False
        )
        
        if movie_title:
            movie = request_for_movie(movie_title)
            title = movie["Title"]
            year = movie["Year"]
            rating = movie["imdbRating"]
            poster_url = movie["Poster"] 
            self.storage._add_movie(title, year, rating, poster_url)
            self._print_color(
                f"Movie '{movie_title}' successfully added!", "green"
            )
            self._enter_to_continue()

    # 3 Delete movie
    def _prompt_user_to_delete_movie(self) -> None:
        """Prompt the user to delete the movie. Deletion only if the
        exact name of the movie is given."""
        print("")
        print("Delete movie:")
        movie_title = self._get_valid_movie_title_from_user(
            case_sensitive=True, reverse=True
        )

        if movie_title:
            self.storage._delete_movie(movie_title)
            self._print_color(
                f"Movie '{movie_title}' successfully deleted!", "green"
            )
            self._enter_to_continue()

    # 4 Update movie
    def _prompt_user_to_update_movie(self) -> None:
        """Prompts user for existing movie, then asks and sets new rating,
        if movie exists.
        """
        movie_title = self._get_valid_movie_title_from_user(
            case_sensitive=False, reverse=True
        )

        if movie_title:
            rating = float(input("Enter a rating (1-10): "))
            self.storage._update_movie(movie_title, rating)
            self._print_color(
                f"Movie '{movie_title}' successfully updated!", "green"
            )
            self._enter_to_continue()

    # 5  Stats
    def _print_movie_stats(self) -> None:
        """Print statistics: average, median, best and worst movie."""
        (
            average,
            median,
            best_movie_rating,
            worst_movie_rating,
            best_movies,
            worst_movies,
        ) = self._get_movie_stats()

        print(f"Average rating: {average:.1f}")
        print(f"Median rating: {median:.1f}")
        self._print_color(
            f"Best movies with awesome {best_movie_rating} rating:"
            + "\n\t"
            + "\n\t".join(best_movies),
            "green",
        )
        self._print_color(
            f"Worst movies with underwhelming {worst_movie_rating}:"
            + "\n\t"
            + "\n\t".join(worst_movies),
            "red",
        )
        self._enter_to_continue()

    def _get_valid_movie_title_from_user(
        self, case_sensitive, reverse=False
    ) -> None | str:
        """Return valid movie title.

        Arguments:
            case_sensitive -- True or False,

        Keyword Arguments:
            reverse --  (default: {False})
            reverse=False returns a movie that does not exist.
            reverse=True returns a movie that exists already.

        Returns:
            valid movie title, except you cancel because movie exists
            or does not exist, depending on reverse boolean.
        """
        while True:
            movie_title = input("Enter a movie name: ")
            if len(movie_title) == 0:
                self._print_color("You must type in a movie!", "red")
                continue

            # when user wants to delete
            # or update a movie it must be an existing movie
            if reverse:
                if not self._movie_exists(movie_title, case_sensitive):
                    self._print_color(
                        "Movie does not exist! Please type the exact movie title",
                        "red",
                    )
                    user_wants_another_movie = (
                        self._ask_user_for_another_movie()
                    )
                    if user_wants_another_movie:
                        continue
                    else:
                        return self._enter_to_continue()
                else:
                    break

            # when user wants to add a movie it must be a new movie
            if not reverse:
                if self._movie_exists(movie_title, case_sensitive):
                    self._print_color("Movie already exist!", "red")
                    user_wants_another_movie = (
                        self._ask_user_for_another_movie()
                    )
                    if user_wants_another_movie:
                        continue
                    else:
                        return self._enter_to_continue()
                else:
                    break
        return movie_title

    def _get_valid_movie_year_from_user(self) -> int:
        """Returns a valid year.Year cannot be below 0 or in the future.

        Returns:
            valid year like: 2023
        """
        while True:
            try:
                year = int(input("Enter first screening year: "))
            except ValueError:
                self._print_color("Input must be an integer!", "red")
            else:
                if year > datetime.datetime.now().year or year < 0:
                    self._print_color(
                        "Year must be a positive number and cannot be in the future!",
                        "red",
                    )
                else:
                    break
        return year

    def _get_valid_movie_rating_from_user(self) -> float:
        """Returns a valid rating.
        Must be a number and has to be between 1-10 including

        Returns:
            valid rating like: 7.8
        """
        while True:
            try:
                rating = float(input("Enter new movie rating (0-10): "))
            except ValueError:
                self._print_color("Input must be a number!", "red")
            else:
                if rating < 0 or rating > 10:
                    self._print_color("Input must be between 0-10!", "red")
                else:
                    break
        return rating

    def _movie_exists(self, movie_title: str, case_sensitive: bool) -> bool:
        """Check if movie exist in database. case_insensitive is on by default.

        Args:
            movie (str):
            case_insensitive (bool, optional): choose for case insensitivity
            Defaults to True.

        Returns:
            bool: True or False
        """
        self.movies = self.storage.get_movie_data()
        if not case_sensitive:
            movies_lower = map(lambda x: x[TITLE].lower(), self.movies)
            return movie_title.lower() in movies_lower
        else:
            movies_og = map(lambda x: x[TITLE], self.movies)
            return movie_title in movies_og

    def _ask_user_for_another_movie(self) -> bool:
        """Ask user if he wants to proceed and enter another movie title
        or to quit.

        Returns:
            True of False
        """
        user_choice = input("Do you want to choose another movie? (y/n): ")
        want_new_movie = True if user_choice.strip().lower() == "y" else False
        if want_new_movie:
            return True
        return False

    def _get_movie_stats(
        self,
    ) -> tuple[float, float, float, float, list[str], list[str]]:
        """Return movie statistics: average rating, median rating,
        best and worst movie rating, best and worst movie

        Returns:
            (average, median, best_movie_rating, worst_movie_rating,
            best_movies, worst_movies)
        """
        ratings = [movie[RATING] for movie in self.movies]

        sorted_movie_ratings = sorted(ratings)
        average = sum(sorted_movie_ratings) / len(self.movies)
        median = statistics.median(sorted_movie_ratings)
        best_movie_rating = max(ratings)
        worst_movie_rating = min(ratings)

        best_movies = [
            movie[TITLE]
            for movie in self.movies
            if movie[RATING] == best_movie_rating
        ]

        worst_movies = [
            movie[TITLE]
            for movie in self.movies
            if movie[RATING] == worst_movie_rating
        ]

        return (
            average,
            median,
            best_movie_rating,
            worst_movie_rating,
            best_movies,
            worst_movies,
        )

    # 6 Random movie
    def _print_random_movie(self) -> None:
        """Process and print a random movie"""
        random_movie_dict = random.choice([movie for movie in self.movies])
        movie_title = random_movie_dict[TITLE]
        movie_rating = random_movie_dict[RATING]
        self._print_color(
            f"Your movie for tonight: {movie_title}, it's rated {movie_rating}",
            "green",
        )
        self._enter_to_continue()

    # 7 Search movie
    def _prompt_user_for_movie_search(self) -> None:
        """Prompt user for a film to search for, or part of a film, then search
        that film in the database and return an exact result or suggestions if not
        found exact movie"""
        search_term = input("Enter full or part of  a movie title: ")
        if search_term:
            self._fuzzy_search(self.movies, search_term)
        else:
            self._print_color(
                "Empty search, type at least one character!", "red"
            )
            return self._prompt_user_for_movie_search()

        self._enter_to_continue()

    def _fuzzy_search(self, movies: list[dict], text: str) -> None:
        """Fuzzy search for movies.

        Args:
            movies (dict[str, float]):
            text (str): movie to search for
        """
        movie_names = [movie[TITLE] for movie in movies]
        fuzzy_results = process.extract(text, movie_names)
        suggestions = [movie for movie, rate in fuzzy_results if rate > 75]
        sub_strings = [
            movie[TITLE]
            for movie in movies
            if text.lower() in movie[TITLE].lower()
        ]
        valid_substrings = set(sub_strings) - (set(suggestions))

        self._print_search_results(text, suggestions, valid_substrings)

    def _print_search_results(
        self, text, suggestions, valid_substrings
    ) -> None:
        """Print search results from fuzzy finder and if any substring is found
        and not already found by fuzzy search it adds additional search results
        that do not met the fuzzy search settings.

        Arguments:
            text -- search term
            suggestions -- fuzzy finder results
            valid_substrings -- additional results if available
        """
        if suggestions:
            self._print_color(
                "We found this:" + "\n\t" + "\n\t".join(suggestions), "green"
            )
        if valid_substrings:
            print("")
            self._print_color(
                f"Maybe your searching this{' as well' if suggestions else ''}:"
                + "\n\t"
                + "\n\t".join(valid_substrings),
                "blue",
            )
        if not suggestions and not valid_substrings:
            self._print_color(f"Nothing with '{text}' found", "red")

    # 8 Movies sorted by rating
    def _print_sorted_movies_by_rating(self) -> None:
        """Print movies based on their ratings. best to worst"""
        return self._print_filtered_movies_by("Rating")

    # 9 Movies sorted by year
    def _print_sorted_movies_by_year(self) -> None:
        """Print movies based on their screening years. New to old"""
        return self._print_filtered_movies_by("Year")

    # 10 Filter movies
    def _prompt_user_to_filter_movies(self) -> None:
        """Print sorted movies based on user choice. You can sort according:
        'Title', 'Year' or 'Rating'
        Additionally you can define the sorting order:
        Descending is default. Add 'asc' to filter item for ascending order."""
        filter_item = input(
            "Filter by ('title', 'year' or 'rating') "
            + "for ascending order type for example: 'year asc':\n"
        )
        filter_item = filter_item.strip().lower()

        if len(filter_item.split()) == 2:
            filter_item, order = filter_item.split()
            if filter_item not in ("title", "year", "rating"):
                self._print_color("Wrong filter name!", "red")
                return self._prompt_user_to_filter_movies()
            if order != "asc":
                self._print_color("Wrong order argument!", "red")
                return self._prompt_user_to_filter_movies()
            return self._print_filtered_movies_by(filter_item, order)
        elif len(filter_item.split()) == 1:
            if filter_item not in ("title", "year", "rating"):
                self._print_color("Wrong filter name!", "red")
                return self._prompt_user_to_filter_movies()
            return self._print_filtered_movies_by(filter_item)
        else:
            self._print_color("Wrong input!", "red")
            return self._prompt_user_to_filter_movies()

        if order:
            return self._print_filtered_movies_by(filter_item, order)
        return self._print_filtered_movies_by(filter_item)

    def _print_filtered_movies_by(
        self, filter_item: str, order: str = "desc"
    ) -> None:
        """Print filtered movies by a specific movie spec. For example by title.
        Optionally you can change the order of sorting.

        Arguments:
            filter_item -- can be 'title', 'year' or 'rating'

        Keyword Arguments:
            order -- optionally you can add asc to the filter item like 'title asc'
            (default: {"desc"})
        """
        sorted_movies = self._sort_movies_by(
            filter_item.capitalize(), order.lower()
        )
        print("")
        for movie in sorted_movies:
            print(f"{movie[TITLE]} ({movie[YEAR]}) {movie[RATING]}")
        self._enter_to_continue()

    def _sort_movies_by(self, filter_item: str, order: str = "desc") -> list:
        """Sorts a copied movie list with chosen filter specs

        Arguments:
            filter_item -- can be 'title', 'year' or 'rating'

        Keyword Arguments:
            order -- optionally you can add asc to the filter item
            like 'title asc'(default: {"desc"})

        Returns:
            _description_
        """

        sorted_movies = sorted(self.movies, key=lambda item: item[filter_item])
        if order == "desc":
            sorted_movies = reversed(sorted_movies)

        return list(sorted_movies)

    def _print_color(self, text, color) -> None:
        """Print colored text in terminal: red, green and blue!"""
        color_translator = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "blue": Fore.BLUE,
        }
        print(f"{color_translator[color]}{text}{Style.RESET_ALL}")

    def _enter_to_continue(self) -> None:
        """Print prompt to continue."""
        print("")
        input("Press enter to continue")
        print("")

    def run(self):
        TITLE = "********** My Movies Database **********"

        MENU_ITEMS = [
            {"i": 0, "command": "Exit", "func": self._print_bye},
            {"i": 1, "command": "List movies", "func": self._print_movie_list},
            {
                "i": 2,
                "command": "Add movie",
                "func": self._prompt_user_to_add_movie,
            },
            {
                "i": 3,
                "command": "Delete movie",
                "func": self._prompt_user_to_delete_movie,
            },
            {
                "i": 4,
                "command": "Update movie",
                "func": self._prompt_user_to_update_movie,
            },
            {"i": 5, "command": "Stats", "func": self._print_movie_stats},
            {
                "i": 6,
                "command": "Random movie",
                "func": self._print_random_movie,
            },
            {
                "i": 7,
                "command": "Search movie",
                "func": self._prompt_user_for_movie_search,
            },
            {
                "i": 8,
                "command": "Movies sorted by rating",
                "func": self._print_sorted_movies_by_rating,
            },
            {
                "i": 9,
                "command": "Movies sorted by year",
                "func": self._print_sorted_movies_by_year,
            },
            {
                "i": 10,
                "command": "Filter movies",
                "func": self._prompt_user_to_filter_movies,
            },
        ]

        app_running = True

        print(TITLE, end="\n\n")
        while app_running:
            os.system("clear")
            self._print_menu(MENU_ITEMS)
            choice = self._get_menu_choice()
            self._call_menu_item(choice, MENU_ITEMS)
            if choice == 0:
                app_running = False

        return MENU_ITEMS

    # MENU
    def _print_menu(self, menu_items: list[dict]) -> None:
        """Print Menu with number and feature.

        Args:
            menu_items (list[dict]): {"menu_item": function}
        """
        print("Menu:")
        print("")

        for menu_item in menu_items:
            print(f"{menu_item['i']}. {menu_item['command']}")
        print("")

    def _get_menu_choice(self) -> int:
        """Prompt user for menu choice

        Returns:
            int: menu number
        """
        while True:
            try:
                while True:
                    choice = int(input("Enter choice (0-10): "))
                    if choice > 10 or choice < 0:
                        self._print_color("Number out of range!", "red")
                    else:
                        break
            except ValueError:
                self._print_color("Only numbers 0-10 are allowed!", "red")
            else:
                return choice

    def _call_menu_item(self, menu_num: int, menu_items: list[dict]):
        """Execute chosen menu function

        Args:
            menu_num (int): menu number (0-10)
            menu_items (list[dict]): dictionary with features and functions

        Returns:
            function to call feature
        """

        return menu_items[menu_num]["func"]()
