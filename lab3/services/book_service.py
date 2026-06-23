from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book import BookCreate, BookStatus
from repository.book_repo import BookRepository
import uuid
from datetime import datetime
from typing import Optional

class BookService:
    def __init__(self, db: AsyncSession):
        self.repo = BookRepository(db)

    async def get_all_books(self, limit: int, cursor: Optional[datetime] = None, status: BookStatus = None, author: str = None, sort_by: str = None):
        return await self.repo.get_all(limit, cursor, status, author, sort_by)

    async def get_book_by_id(self, book_id: str):
        return await self.repo.get_by_id(book_id)

    async def create_book(self, book_in: BookCreate):
        book_dict = book_in.model_dump()
        book_dict["id"] = str(uuid.uuid4())
        return await self.repo.create(book_dict)

    async def delete_book(self, book_id: str):
        await self.repo.delete(book_id)