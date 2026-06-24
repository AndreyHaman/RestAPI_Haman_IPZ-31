from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from pydantic_mongo import PydanticObjectId

class BookRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("books_collection")

    async def get_all(self, limit: int, offset: int) -> List[dict]:
        cursor = self.collection.find({}).skip(offset).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_by_id(self, book_id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": PydanticObjectId(book_id)})

    async def create(self, book_data: dict) -> dict:
        result = await self.collection.insert_one(book_data)
        return await self.get_by_id(result.inserted_id)

    async def delete(self, book_id: str) -> bool:
        response = await self.collection.delete_one({"_id": PydanticObjectId(book_id)})
        return response.deleted_count > 0