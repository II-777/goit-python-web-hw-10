import json
from bson.objectid import ObjectId
from pymongo import MongoClient

# Connect to the MongoDB server running on localhost
client = MongoClient("mongodb://localhost")

# Select the "hw" database
db = client.hw

# Open the 'quotes.json' file in read mode with UTF-8 encoding
with open('quotes.json', 'r', encoding='utf-8') as file:
    # Load the JSON data from the file into the 'quotes' variable
    quotes = json.load(file)

# Iterate through each quote in the loaded JSON data
for quote in quotes:
    # Query the 'authors' collection to find an author with the specified full name
    author = db.authors.find_one({'fullname': quote['author']})

    # Check if an author is found
    if author:
        # Insert a new document into the 'quotes' collection with quote text, tags, and a reference to the author
        db.quotes.insert_one({
            'quote': quote['quote'],
            'tags': quote['tags'],
            'author': ObjectId(author['_id'])
        })
