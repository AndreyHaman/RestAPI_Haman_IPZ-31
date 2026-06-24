from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.book import BookCreate
from repository.book_repo import BookRepository

class BookService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = BookRepository(db)

    async def get_all_books(self, limit: int, offset: int):
        return await self.repo.get_all(limit, offset)

    async def get_book_by_id(self, book_id: str):
        return await self.repo.get_by_id(book_id)

    async def create_book(self, book_in: BookCreate):
        book_dict = book_in.model_dump()
        return await self.repo.create(book_dict)

    async def delete_book(self, book_id: str):
        return await self.repo.delete(book_id)