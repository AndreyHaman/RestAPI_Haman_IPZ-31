import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@localhost:27017")

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database():
    return db.client.books