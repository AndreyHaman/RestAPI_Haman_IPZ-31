from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.endpoints import router as books_router
from core.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Library PostgreSQL API", lifespan=lifespan)

app.include_router(books_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")