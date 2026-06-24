from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("users_collection")

    async def get_by_username(self, username: str) -> Optional[dict]:
        return await self.collection.find_one({"username": username})

    async def create(self, user_data: dict) -> dict:
        result = await self.collection.insert_one(user_data)
        return await self.collection.find_one({"_id": result.inserted_id})