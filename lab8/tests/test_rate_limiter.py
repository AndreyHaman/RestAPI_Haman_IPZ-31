import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from mongomock_motor import AsyncMongoMockClient
import fakeredis

from main import app
from core.database import db
from core import rate_limiter

@pytest_asyncio.fixture(autouse=True)
async def setup_environment():
    db.client = AsyncMongoMockClient()

    rate_limiter.redis_client = fakeredis.FakeAsyncRedis(decode_responses=True)
    
    yield

    await db.client.drop_database('books')
    await rate_limiter.redis_client.flushall()

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_anonymous_rate_limit(async_client: AsyncClient):
    response_1 = await async_client.get("/books/")
    assert response_1.status_code == 200

    response_2 = await async_client.get("/books/")
    assert response_2.status_code == 200

    response_3 = await async_client.get("/books/")
    assert response_3.status_code == 429
    assert response_3.json()["detail"] == "Too many requests"

@pytest.mark.asyncio
async def test_authenticated_rate_limit(async_client: AsyncClient):
    payload = {"username": "rate_user", "password": "superpassword"}
    await async_client.post("/auth/register", json=payload)
    login_res = await async_client.post("/auth/login", json=payload)
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}

    for _ in range(10):
        response = await async_client.get("/books/", headers=headers)
        assert response.status_code == 200

    response_11 = await async_client.get("/books/", headers=headers)
    assert response_11.status_code == 429
    assert response_11.json()["detail"] == "Too many requests"