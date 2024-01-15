from pymongo import MongoClient


def get_mongodb():
    # Connect to the MongoDB server running on localhost
    client = MongoClient("mongodb://localhost")
    # Select the "hw" database
    db = client.hw

    return db
