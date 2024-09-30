import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI", None)

client = MongoClient(uri)
db = client[os.getenv("MONGO_DB_NAME")]

test_collection = db["test"]
