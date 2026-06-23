from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from uuid import UUID

class BookStatus(str, Enum):
    AVAILABLE = "available"
    ISSUED = "issued"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: str = Field(...)
    status: BookStatus = Field(default=BookStatus.AVAILABLE)
    year: int = Field(..., gt=0)

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)