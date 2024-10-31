"""
CLI menu for managing a movie database.

The `Menu` class displays options, captures user choices, and triggers
corresponding functions from a provided function table.
"""

import utility as helper

MENU_ITEMS = [
    "Exit",
    "List movies",
    "Add movie",
    "Delete movie",
    "Stats",
    "Random movie",
    "Search movie",
    "Movies sorted by rating",
    "Movies sorted by year",
    "Filter movies",
    "Generate website",
]


class Menu:
    """Handles menu display and action execution for movie database tasks.

    Attributes:
        menu_items (list): Available menu options.
        function_table (dict): Maps menu options to their associated functions.
    """

    def __init__(self, function_table) -> None:
        self.menu_items = MENU_ITEMS
        self.function_table = function_table

    def print_menu(self) -> None:
        """Displays all menu options with their corresponding numbers."""
        print("Menu:\n")
        for i, menu_item in enumerate(self.menu_items):
            print(f"{i}. {menu_item}")
        print("")

    def get_menu_choice(self) -> int:
        """Prompts the user to select a menu option.

        Returns:
            int: The selected menu number.
        """
        while True:
            try:
                while True:
                    choice = int(input("Enter choice (0-10): "))
                    if choice > 10 or choice < 0:
                        helper.print_color("Number out of range!", "red")
                    else:
                        break
            except ValueError:
                helper.print_color("Only numbers 0-10 are allowed!", "red")
            else:
                return choice

    def call_menu_item(self, menu_num: int):
        """Executes the function associated with the chosen menu item.

        Args:
            menu_num (int): The selected menu number.

        Returns:
            Any: The result of the function call
            associated with the menu option.
        """
        command = self.menu_items[menu_num]
        function = self.function_table[command]
        return function()
