from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DATABASE_NAME")]

ramos_collection = db["ramos"]
ratings_collection = db["ratings"]
comments_collection = db["comments"]
users_collection = db["users"]
