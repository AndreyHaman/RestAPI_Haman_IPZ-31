from pymongo.database import Database
from typing import List, Optional
from pydantic_mongo import PydanticObjectId

class BookRepository:
    def __init__(self, db: Database):
        self.collection = db.get_collection("books_collection")

    def get_all(self, limit: int, offset: int) -> List[dict]:
        cursor = self.collection.find({}).skip(offset).limit(limit)
        return list(cursor)

    def get_by_id(self, book_id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": PydanticObjectId(book_id)})

    def create(self, book_data: dict) -> dict:
        result = self.collection.insert_one(book_data)
        return self.get_by_id(result.inserted_id)

    def delete(self, book_id: str) -> bool:
        response = self.collection.delete_one({"_id": PydanticObjectId(book_id)})
        return response.deleted_count > 0