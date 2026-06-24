import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from mongomock_motor import AsyncMongoMockClient

from main import app
from core.database import get_database

mock_client = AsyncMongoMockClient()
mock_db = mock_client.test_books_db

async def override_get_database():
    return mock_db

app.dependency_overrides[get_database] = override_get_database

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Очищає фейкову колекцію перед і після кожного тесту"""
    await mock_db.books_collection.drop()
    yield
    await mock_db.books_collection.drop()

@pytest_asyncio.fixture
async def async_client():
    """Клієнт для симуляції запитів до API"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_book(async_client: AsyncClient):
    payload = {
        "title": "Mongo Book", 
        "author": "Test Author", 
        "description": "Desc", 
        "status": "available", 
        "year": 2024
    }
    response = await async_client.post("/books/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mongo Book"
    assert "_id" in data

@pytest.mark.asyncio
async def test_pagination_limit_offset(async_client: AsyncClient):
    for i in range(3):
        payload = {"title": f"Book {i}", "author": "A", "description": "D", "status": "available", "year": 2000}
        await async_client.post("/books/", json=payload)

    response_1 = await async_client.get("/books/?limit=2&offset=0")
    assert response_1.status_code == 200
    data_1 = response_1.json()
    assert len(data_1) == 2
    assert data_1[0]["title"] == "Book 0"

    response_2 = await async_client.get("/books/?limit=2&offset=2")
    assert response_2.status_code == 200
    data_2 = response_2.json()
    assert len(data_2) == 1 
    assert data_2[0]["title"] == "Book 2"