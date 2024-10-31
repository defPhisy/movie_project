"""
Utility module for printing colored text in the terminal and pausing execution.

Functions:
- print_color(text: str, color: str) -> None: Prints text in red, green, or blue.
- enter_to_continue() -> None: Prompts user to press Enter to continue.
"""

from colorama import Fore, Style


def print_color(text: str, color: str) -> None:
    """Print colored text in terminal: red, green, and blue!"""
    color_translator = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "blue": Fore.BLUE,
    }
    print(f"{color_translator[color]}{text}{Style.RESET_ALL}")


def enter_to_continue() -> None:
    """Print prompt to continue."""
    print("")
    input("Press enter to continue")
    print("")
