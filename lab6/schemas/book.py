from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from pydantic_mongo import PydanticObjectId

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
    id: PydanticObjectId = Field(alias="_id") 

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)