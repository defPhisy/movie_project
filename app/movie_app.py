"""
A movie management application.

Features include adding, deleting, searching, and filtering movies,
viewing statistics, random movie suggestions, and generating an HTML website.
"""

import datetime
import os
import random
import re
import statistics

import utility as helper
from storage.istorage import RATING, TITLE, YEAR
from menu import Menu
from movie_api import request_for_movie
from thefuzz import process


class MovieApp:
    TITLE = "********** My Movies Database **********"

    def __init__(self, storage) -> None:
        self.storage = storage
        self.movies = self.storage.get_movie_data()
        self.menu_actions = Menu({
            "Exit": self._print_bye,
            "List movies": self._print_movie_list,
            "Add movie": self._prompt_user_to_add_movie,
            "Delete movie": self._prompt_user_to_delete_movie,
            "Stats": self._print_movie_stats,
            "Random movie": self._print_random_movie,
            "Search movie": self._prompt_user_for_movie_search,
            "Movies sorted by rating": self._print_sorted_movies_by_rating,
            "Movies sorted by year": self._print_sorted_movies_by_year,
            "Filter movies": self._prompt_user_to_filter_movies,
            "Generate website": self._generate_website,
        })

    def _update_movies(self) -> None:
        self.movies = self.storage.get_movie_data()

    # 0 Exit
    def _print_bye(self) -> None:
        """Print 'Good Bye' before program exits"""
        print("")
        helper.print_color("Good Bye", "blue")
        print("")
        quit()

    # 1 List movies
    def _print_movie_list(self) -> None:
        """Print all movies in database."""
        self._update_movies()
        print("")
        print(len(self.movies), "movies in total")
        for movie in self.movies:
            print(f"{movie[TITLE]} ({movie[YEAR]}): {movie[RATING]}")

        helper.enter_to_continue()

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
            if movie["Response"] == "True":  # does not return bool
                title = movie["Title"]
                year = movie["Year"]
                rating = movie["imdbRating"]
                poster_url = movie["Poster"]
                imdb_id = movie["imdbID"]
                self.storage._add_movie(
                    title, year, rating, poster_url, imdb_id
                )
                helper.print_color(
                    f"Movie '{title}' successfully added!", "green"
                )
                helper.enter_to_continue()
            else:
                error_msg = movie["Error"]
                helper.print_color(error_msg, "red")
                helper.enter_to_continue()

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
            helper.print_color(
                f"Movie '{movie_title}' successfully deleted!", "green"
            )
            helper.enter_to_continue()

    # 4  Stats
    def _print_movie_stats(self) -> None:
        """Print statistics: average, median, best and worst movie."""
        try:
            (
                average,
                median,
                best_movie_rating,
                worst_movie_rating,
                best_movies,
                worst_movies,
            ) = self._get_movie_stats()
        except ValueError as error:
            helper.print_color(f"{error}", "red")
            helper.enter_to_continue()
        else:
            print(f"Average rating: {average:.1f}")
            print(f"Median rating: {median:.1f}")
            helper.print_color(
                f"Best movies with awesome {best_movie_rating} rating:"
                + "\n\t"
                + "\n\t".join(best_movies),
                "green",
            )
            helper.print_color(
                f"Worst movies with underwhelming {worst_movie_rating}:"
                + "\n\t"
                + "\n\t".join(worst_movies),
                "red",
            )
            helper.enter_to_continue()

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
                helper.print_color("You must type in a movie!", "red")
                continue

            # when user wants to delete
            # or update a movie it must be an existing movie
            if reverse:
                if not self._movie_exists(movie_title, case_sensitive):
                    helper.print_color(
                        "Movie does not exist! Please type the exact movie title",
                        "red",
                    )
                    user_wants_another_movie = (
                        self._ask_user_for_another_movie()
                    )
                    if user_wants_another_movie:
                        continue
                    else:
                        return helper.enter_to_continue()
                else:
                    break

            # when user wants to add a movie it must be a new movie
            if not reverse:
                if self._movie_exists(movie_title, case_sensitive):
                    helper.print_color("Movie already exist!", "red")
                    user_wants_another_movie = (
                        self._ask_user_for_another_movie()
                    )
                    if user_wants_another_movie:
                        continue
                    else:
                        return helper.enter_to_continue()
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
                helper.print_color("Input must be an integer!", "red")
            else:
                if year > datetime.datetime.now().year or year < 0:
                    helper.print_color(
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
                helper.print_color("Input must be a number!", "red")
            else:
                if rating < 0 or rating > 10:
                    helper.print_color("Input must be between 0-10!", "red")
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
        self._update_movies()
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
        self._update_movies()

        if len(self.movies) < 2:
            raise ValueError(
                "Not enough movies in database!"
                + "To perform stats you need at least 2 movies."
            )
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

    # 5 Random movie
    def _print_random_movie(self) -> None:
        """Process and print a random movie"""
        self._update_movies()
        try:
            random_movie_dict = random.choice([movie for movie in self.movies])
        except IndexError:
            helper.print_color("No movies in database to choose from!", "red")
        else:
            movie_title = random_movie_dict[TITLE]
            movie_rating = random_movie_dict[RATING]
            helper.print_color(
                f"Your movie for tonight: {movie_title}, it's rated {movie_rating}",
                "green",
            )
        helper.enter_to_continue()

    # 6 Search movie
    def _prompt_user_for_movie_search(self) -> None:
        """Prompt user for a film to search for, or part of a film, then search
        that film in the database and return an exact result or suggestions
        if not found exact movie"""
        self._update_movies()
        search_term = input("Enter full or part of  a movie title: ")
        if search_term:
            self._fuzzy_search(self.movies, search_term)
        else:
            helper.print_color(
                "Empty search, type at least one character!", "red"
            )
            return self._prompt_user_for_movie_search()

        helper.enter_to_continue()

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
            helper.print_color(
                "We found this:" + "\n\t" + "\n\t".join(suggestions), "green"
            )
        if valid_substrings:
            print("")
            helper.print_color(
                f"Maybe your searching this{' as well' if suggestions else ''}:"
                + "\n\t"
                + "\n\t".join(valid_substrings),
                "blue",
            )
        if not suggestions and not valid_substrings:
            helper.print_color(f"Nothing with '{text}' found", "red")

    # 7 Movies sorted by rating
    def _print_sorted_movies_by_rating(self) -> None:
        """Print movies based on their ratings. best to worst"""
        return self._print_filtered_movies_by("Rating")

    # 8 Movies sorted by year
    def _print_sorted_movies_by_year(self) -> None:
        """Print movies based on their screening years. New to old"""
        return self._print_filtered_movies_by("Year")

    # 9 Filter movies
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
                helper.print_color("Wrong filter name!", "red")
                return self._prompt_user_to_filter_movies()
            if order != "asc":
                helper.print_color("Wrong order argument!", "red")
                return self._prompt_user_to_filter_movies()
            return self._print_filtered_movies_by(filter_item, order)
        elif len(filter_item.split()) == 1:
            if filter_item not in ("title", "year", "rating"):
                helper.print_color("Wrong filter name!", "red")
                return self._prompt_user_to_filter_movies()
            return self._print_filtered_movies_by(filter_item)
        else:
            helper.print_color("Wrong input!", "red")
            return self._prompt_user_to_filter_movies()

    def _print_filtered_movies_by(
        self, filter_item: str, order: str = "desc"
    ) -> None:
        """Print filtered movies by a specific movie spec. For example by title.
        Optionally you can change the order of sorting.

        Arguments:
            filter_item -- can be 'title', 'year' or 'rating'

        Keyword Arguments:
            order -- optionally you can add asc to the filter item
            like 'title asc'
            (default: {"desc"})
        """
        sorted_movies = self._sort_movies_by(
            filter_item.capitalize(), order.lower()
        )
        print("")
        for movie in sorted_movies:
            print(f"{movie[TITLE]} ({movie[YEAR]}) {movie[RATING]}")
        helper.enter_to_continue()

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
        self._update_movies()
        sorted_movies = sorted(self.movies, key=lambda item: item[filter_item])
        if order == "desc":
            sorted_movies = reversed(sorted_movies)

        return list(sorted_movies)

    # 10 Generate Website
    def _generate_website(self):
        template_file = "app/static/templates/index_template.html"
        website = "app/static/index.html"
        website_title = input("Type a website heading: ")
        with open(template_file, "r") as file:
            data = file.read()

        movie_html = self._generate_movie_html()
        template_html = data

        translation_table = {
            "__TEMPLATE_TITLE__": website_title,
            "__TEMPLATE_MOVIE_GRID__": movie_html,
        }
        website_html = re.sub(
            "|".join([word for word in translation_table]),
            lambda x: translation_table[x.group()],
            template_html,
        )

        # save new generated index.html
        with open(website, "w") as file:
            file.write(website_html)
        helper.print_color("Website was generated successfully.", "green")
        helper.enter_to_continue()

    def _generate_movie_html(self):
        self._update_movies()
        html_template = self.get_movie_html_template()
        final_html = ""

        for movie in self.movies:
            translation_table = {
                "__POSTER__": movie["Poster"],
                "__TITLE__": movie["Title"],
                "__YEAR__": str(movie["Year"]),
                "__STARS__": round(int(movie["Rating"] // 2)) * "⭐",
                "__LINK__": movie["ID"],
            }

            movie_html = re.sub(
                "|".join([word for word in translation_table]),
                lambda x: translation_table[x.group()],
                html_template,
            )
            final_html += movie_html
        return final_html

    def get_movie_html_template(self):
        movie_html_template = "app/static/templates/movie_template.html"
        with open(movie_html_template, "r") as file:
            return file.read()

    def _get_stars(self):
        pass

    def run(self):
        app_running = True

        print(TITLE, end="\n\n")
        while app_running:
            os.system("clear")
            self.menu_actions.print_menu()
            choice = self.menu_actions.get_menu_choice()
            self.menu_actions.call_menu_item(choice)
