from colorama import Fore, Style


def print_color(text, color) -> None:
    """Print colored text in terminal: red, green and blue!"""
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
