from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["mydatabase"]
collection = db["products"]

product_list = [
    {"name": "Хліб", "price": 42.0, "quantity": 21},
    {"name": "Молоко", "price": 60.0, "quantity": 125},
    {"name": "Кефір", "price": 92.0, "quantity": 78}
]
collection.insert_many(product_list)

for product in collection.find():
    print(product)

collection.update_many({}, {"$set": {"status": "old"}})

print("_$_" * 27)
for product in collection.find():
    print(product)

collection.update_many({"price": {"$gt": 59}}, {"$set": {"status": "new"}})

collection.update_one({"name": "Хліб"}, {"$set": {"price": 46.0}})

print("_$_" * 27)
for product in collection.find():
    print(product)

collection.delete_many({})
