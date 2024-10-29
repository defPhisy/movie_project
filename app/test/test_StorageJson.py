from movie_app import MovieApp
from storage_json import StorageJson



storage = StorageJson('app/data/movie_db.json')
movie_app = MovieApp(storage)
movie_app.run()
# app.print_bye()
# app.print_movie_list()
# app.prompt_user_to_add_movie()
# app.prompt_user_to_delete_movie()
# app.prompt_user_to_update_movie()
# app.print_movie_stats()