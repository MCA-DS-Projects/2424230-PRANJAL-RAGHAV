from pymongo import MongoClient
from backend.config import Config


# Initialize MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client["nutraexpert"]

# Create collections
users_collection = db["users"]
