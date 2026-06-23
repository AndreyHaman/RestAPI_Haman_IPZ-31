from sqlalchemy import Column, String, Integer, Enum as SQLEnum, DateTime
from sqlalchemy.sql import func
import uuid
from core.database import Base
from schemas.book import BookStatus

class BookORM(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(SQLEnum(BookStatus), default=BookStatus.AVAILABLE, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)