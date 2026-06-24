from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from core.database import get_database
from schemas.book import BookCreate, BookResponse
from services.book_service import BookService
from core.security import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

async def get_book_service(db = Depends(get_database)):
    return BookService(db)

@router.get("/", response_model=List[BookResponse], response_model_by_alias=False)
async def get_books(
    limit: int = 10, 
    offset: int = 0, 
    service: BookService = Depends(get_book_service),
    current_user: str = Depends(get_current_user)
):
    return await service.get_all_books(limit, offset)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def create_book(
    book_in: BookCreate, 
    service: BookService = Depends(get_book_service),
    current_user: str = Depends(get_current_user)
):
    return await service.create_book(book_in)

@router.get("/{book_id}", response_model=BookResponse, response_model_by_alias=False)
async def get_book(
    book_id: str, 
    service: BookService = Depends(get_book_service),
    current_user: str = Depends(get_current_user)
):
    book = await service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str, 
    service: BookService = Depends(get_book_service),
    current_user: str = Depends(get_current_user)
):
    deleted = await service.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return None