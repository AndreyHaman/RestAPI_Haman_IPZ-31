import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from core.database import get_database
from repository.user_repo import UserRepository
from schemas.user import UserCreate, UserResponse, TokenResponse, RefreshTokenRequest
from core.security import (
    get_password_hash, verify_password, 
    create_access_token, create_refresh_token, 
    SECRET_KEY, ALGORITHM
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def register(user_in: UserCreate, db = Depends(get_database)):
    repo = UserRepository(db)
    existing_user = await repo.get_by_username(user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Користувач з таким ім'ям вже існує")
    
    user_data = {
        "username": user_in.username,
        "hashed_password": get_password_hash(user_in.password)
    }
    new_user = await repo.create(user_data)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(user_in: UserCreate, db = Depends(get_database)):
    repo = UserRepository(db)
    user = await repo.get_by_username(user_in.username)
    if not user or not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Неправильне ім'ям користувача або пароль")
    
    return {
        "access_token": create_access_token(user["username"]),
        "refresh_token": create_refresh_token(user["username"])
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(payload: RefreshTokenRequest):
    try:
        decoded_payload = jwt.decode(payload.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Невалідний тип токена")
        
        username: str = decoded_payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Невалідний токен")
            
        return {
            "access_token": create_access_token(username),
            "refresh_token": create_refresh_token(username)
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Термін дії refresh токена вичерпано. Увійдіть знову")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Невалідний refresh токен")