from models.data import books_db
from typing import List, Dict, Optional

class BookRepository:
    async def get_all(self) -> List[Dict]:
        return books_db

    async def get_by_id(self, book_id: str) -> Optional[Dict]:
        for book in books_db:
            if book["id"] == book_id:
                return book
        return None

    async def add(self, book_data: Dict) -> Dict:
        books_db.append(book_data)
        return book_data

    async def delete(self, book_id: str) -> None:
        for i, book in enumerate(books_db):
            if book["id"] == book_id:
                del books_db[i]
                break