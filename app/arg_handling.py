import argparse

parser = argparse.ArgumentParser(description="Movie DB")
parser.add_argument(
    "-j",
    "--json",
    action="store_true",
    help="start app with json storage for movies, this argument is the default storage setting you can omit it!",
)
parser.add_argument(
    "-c",
    "--csv",
    action="store_true",
    help="start app with csv storage for movies, without this argument app starts with default json storage",
)
parser.add_argument(
    "-n",
    "--name",
    type=str,
    help="set storage name, default name is 'movie_db' ",
)
args = parser.parse_args()
