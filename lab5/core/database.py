import os
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@localhost:27017")

class Database:
    client: MongoClient = None

db = Database()

def init_db():
    db.client = MongoClient(MONGO_URL)

def get_database():
    return db.client.books