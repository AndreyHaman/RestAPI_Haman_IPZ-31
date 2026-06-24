from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

from api.endpoints import router as books_router
from core.database import db, MONGO_URL

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ініціалізація Mongo клієнта при старті
    db.client = AsyncIOMotorClient(MONGO_URL)
    print("Успішно підключено до MongoDB!")
    yield
    # Закриваємо з'єднання при вимкненні
    db.client.close()

app = FastAPI(title="Library MongoDB API", lifespan=lifespan)

app.include_router(books_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")