from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", None)
MONGO_DB_URI = os.getenv("MONGO_DB_URI", None)

assert MONGO_DB_NAME is not None, "DATABASE_NAME is not set"
assert MONGO_DB_URI is not None, "MONGO_DB_URI is not set"

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]
ramos_collection = db["ramos"]
accounts_collection = db["accounts"]