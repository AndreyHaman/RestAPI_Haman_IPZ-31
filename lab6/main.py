from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
import os

from core.database import db
from api.endpoints import router as book_router
from api.auth import router as auth_router

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo_admin:password@localhost:27017")

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.client = AsyncIOMotorClient(MONGO_URL)
    yield
    db.client.close()

app = FastAPI(title="Library Async API with Auth", lifespan=lifespan)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(auth_router)
app.include_router(book_router)