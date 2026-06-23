import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from main import app
from core.database import get_db, Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session
app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_book(async_client: AsyncClient):
    payload = {"title": "Test", "author": "Author", "description": "D", "status": "available", "year": 2024}
    response = await async_client.post("/books/", json=payload)
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_pagination(async_client: AsyncClient):
    for i in range(3):
        payload = {"title": f"Book {i}", "author": "A", "description": "D", "status": "available", "year": 2000}
        await async_client.post("/books/", json=payload)
    response = await async_client.get("/books/?limit=2&offset=0")
    assert len(response.json()) == 2