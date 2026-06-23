from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from models.book_orm import BookORM
from typing import List, Optional

class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, limit: int, offset: int, status: str = None, author: str = None, sort_by: str = None) -> List[BookORM]:
        query = select(BookORM)
        
        if status:
            query = query.where(BookORM.status == status)
        if author:
            query = query.where(BookORM.author.ilike(f"%{author}%"))
            
        if sort_by == "title":
            query = query.order_by(BookORM.title)
        elif sort_by == "year":
            query = query.order_by(BookORM.year)

        query = query.offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, book_id: str) -> Optional[BookORM]:
        result = await self.db.execute(select(BookORM).where(BookORM.id == book_id))
        return result.scalars().first()

    async def create(self, book_data: dict) -> BookORM:
        new_book = BookORM(**book_data)
        self.db.add(new_book)
        await self.db.commit()
        await self.db.refresh(new_book)
        return new_book

    async def delete(self, book_id: str) -> None:
        await self.db.execute(delete(BookORM).where(BookORM.id == book_id))
        await self.db.commit()