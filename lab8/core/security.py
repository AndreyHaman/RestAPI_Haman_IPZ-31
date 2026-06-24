import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "super_secret_key_for_library_api_v1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_bearer = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(username: str) -> str:
    return create_token({"sub": username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access")

def create_refresh_token(username: str) -> str:
    return create_token({"sub": username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), "refresh")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security_bearer)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Невалідний тип токена. Очікується access токен")
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Токен не містить користувача")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Термін дії access токена вичерпано")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Невалідний access токен")

async def get_optional_user(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") == "access":
            return payload.get("sub")
    except:
        pass
    return None