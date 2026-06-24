from pymongo.database import Database
from schemas.book import BookCreate
from repository.book_repo import BookRepository

class BookService:
    def __init__(self, db: Database):
        self.repo = BookRepository(db)

    def get_all_books(self, limit: int, offset: int):
        return self.repo.get_all(limit, offset)

    def get_book_by_id(self, book_id: str):
        return self.repo.get_by_id(book_id)

    def create_book(self, book_in: BookCreate):
        book_dict = book_in.model_dump()
        return self.repo.create(book_dict)

    def delete_book(self, book_id: str):
        return self.repo.delete(book_id)