from fastapi import APIRouter, HTTPException, Depends, status, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from schemas.book import BookCreate, BookResponse
from services.book_service import BookService
from core.database import get_database

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(
    db: AsyncIOMotorDatabase = Depends(get_database),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return await BookService(db).get_all_books(limit, offset)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    book = await BookService(db).get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await BookService(db).create_book(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    deleted = await BookService(db).delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книгу не знайдено або вже видалено")
    return None