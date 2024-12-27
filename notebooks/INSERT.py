import json
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
ratings_collection = db["ratings"]

with open("./ofg.json", 'r') as f:
    data = json.load(f)

if isinstance(data, list):
    for ramo_obj in data:
        result = ramos_collection.insert_one(ramo_obj)
else:
    print("El archivo JSON no contiene un array de objetos.")
