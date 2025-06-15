import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection URI from environment variables
mongo_uri = os.getenv("MONGO_URI")

# Create MongoDB client
client = MongoClient(mongo_uri)

# Get database
db = client.get_database("sample_db")

# Get collection
items_collection = db.get_collection("items")