from repository.book_repo import BookRepository
from schemas.book import BookCreate, BookStatus
from uuid import uuid4
from typing import List, Optional

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_all_books(
        self, 
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None, 
        sort_by: Optional[str] = None
    ) -> List[dict]:
        books = await self.repo.get_all()

        # Фільтрація
        if status:
            books = [b for b in books if b["status"] == status.value]
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]

        # Сортування
        if sort_by == "title":
            books.sort(key=lambda x: x["title"])
        elif sort_by == "year":
            books.sort(key=lambda x: x["year"])

        return books

    async def get_book(self, book_id: str) -> Optional[dict]:
        return await self.repo.get_by_id(book_id)

    async def create_book(self, book_data: BookCreate) -> dict:
        new_book = book_data.model_dump()
        new_book["id"] = str(uuid4()) # Генеруємо UUID
        return await self.repo.add(new_book)

    async def delete_book(self, book_id: str) -> None:
        await self.repo.delete(book_id)