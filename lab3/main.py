from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from api.endpoints import router as books_router
from core.database import engine, Base

# Сучасний спосіб створення таблиць при запуску сервера
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Тут сервер працює і приймає запити

# Підключаємо lifespan до нашого додатку
app = FastAPI(title="Library PostgreSQL API", lifespan=lifespan)

app.include_router(books_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")