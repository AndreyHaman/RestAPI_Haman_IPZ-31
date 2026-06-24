from pydantic import BaseModel, Field, ConfigDict
from pydantic_mongo import PydanticObjectId

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)

class UserResponse(UserBase):
    id: PydanticObjectId = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str