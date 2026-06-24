from fastapi import APIRouter, Depends, status, HTTPException, Request
from typing import List
from core.database import get_database
from schemas.book import BookCreate, BookResponse
from services.book_service import BookService
from core.security import get_current_user, get_optional_user
from core.rate_limiter import rate_limit 

router = APIRouter(prefix="/books", tags=["Books"])

async def get_book_service(db = Depends(get_database)):
    return BookService(db)

async def check_rate_limit(request: Request, user_id: str | None = Depends(get_optional_user)):
    await rate_limit(request, user_id)

@router.get("/", response_model=List[BookResponse], response_model_by_alias=False, dependencies=[Depends(check_rate_limit)])
async def get_books(
    limit: int = 10, 
    offset: int = 0, 
    service: BookService = Depends(get_book_service)
):
    return await service.get_all_books(limit, offset)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_rate_limit)])
async def create_book(
    book_in: BookCreate, 
    service: BookService = Depends(get_book_service),
    current_user: str = Depends(get_current_user)
):
    return await service.create_book(book_in)

@router.get("/{book_id}", response_model=BookResponse, response_model_by_alias=False, dependencies=[Depends(check_rate_limit)])
async def get_book(
    book_id: str, 
    service: BookService = Depends(get_book_service)
):
    book = await service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_rate_limit)])
async def delete_book(
    book_id: str, 
    service: BookService = Depends(get_book_service),
    current_user: str = Depends(get_current_user)
):
    deleted = await service.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return None