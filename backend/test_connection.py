from config import Config
from pymongo import MongoClient

try:
    client = MongoClient(Config.MONGO_URI)
    db = client.get_database("nutraexpert")
    print("✅ Connected to MongoDB successfully!")
    print("Databases:", client.list_database_names())
except Exception as e:
    print("❌ Connection failed:", e)
