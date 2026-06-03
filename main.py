from fastapi import FastAPI
from api.endpoints import router as books_router

app = FastAPI(title="Library REST API", description="Лабораторна робота 1")
app.include_router(books_router)