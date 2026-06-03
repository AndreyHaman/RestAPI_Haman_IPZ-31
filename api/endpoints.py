from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from schemas.book import BookResponse, BookCreate, BookStatus
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
book_service = BookService()

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(
    status: Optional[BookStatus] = None,
    author: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="Сортування: 'title' або 'year'")
):
    return await book_service.get_all_books(status, author, sort_by)

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID):
    book = await book_service.get_book(str(book_id))
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    return await book_service.create_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID):
    # Ідемпотентний DELETE: ми завжди повертаємо 204 (Успіх, немає контенту).
    # Незалежно від того, чи була книга в базі до цього запиту, 
    # фінальний стан системи однаковий - книги з таким ID більше немає.
    await book_service.delete_book(str(book_id))
    return None