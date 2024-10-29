import storage_json


storage = storage_json.StorageJson("app/data/movie_db.json")
print(storage.list_movies())
storage.add_movie("Hurz", "1992", 3.7, "poster1")
storage.add_movie("Furz", "2992", 4.7, "poster2")
print(storage.list_movies())
storage.delete_movie("Furz")
storage.update_movie("Hurz", 10)
print(storage.list_movies())
