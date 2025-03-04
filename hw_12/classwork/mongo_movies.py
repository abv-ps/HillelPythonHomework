from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["movie_database"]
collection = db["movies"]

movies = [
    {"title": "The Dark Knight", "release_year": 2008, "genre": "Action", "rate": 8.0},
    {"title": "Inception", "release_year": 2010, "genre": "Sci-Fi", "rate": 8.2},
    {"title": "The Matrix", "release_year": 1999, "genre": "Sci-Fi", "rate": 9.2},
    {"title": "Forrest Gump", "release_year": 1994, "genre": "Drama", "rate": 8.7},
    {"title": "Pulp Fiction", "release_year": 1994, "genre": "Crime", "rate": 6.2},
    {"title": "The Shawshank Redemption", "release_year": 1994, "genre": "Drama", "rate": 9.1},
    {"title": "The Godfather", "release_year": 1972, "genre": "Crime", "rate": 9.7},
    {"title": "Fight Club", "release_year": 1999, "genre": "Drama", "rate": 7.2},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "release_year": 2001, "genre": "Fantasy", "rate": 8.5},
    {"title": "The Lion King", "release_year": 1994, "genre": "Animation", "rate": 9.4},
    {"title": "Interstellar", "release_year": 2014, "genre": "Sci-Fi", "rate": 8.7}
]

collection.insert_many(movies)

print("_$_" * 27)
for movie in collection.find():
    print(movie)
collection.update_many(
    {"release_year": {"$lt": 2000}, "rate": {"$gt": 9}},
    {"$inc": {"rate": 0.5}}
)
print("_$_" * 27)
for movie in collection.find():
    print(movie)

collection.delete_many({})