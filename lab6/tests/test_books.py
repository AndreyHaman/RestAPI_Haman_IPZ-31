import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from mongomock_motor import AsyncMongoMockClient

from main import app
from core.database import db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    db.client = AsyncMongoMockClient()
    yield
    await db.client.drop_database('books')

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    payload = {"username": "test_user", "password": "superpassword"}
    response = await async_client.post("/auth/register", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "test_user"

@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    payload = {"username": "test_user", "password": "superpassword"}
    await async_client.post("/auth/register", json=payload)
 
    response = await async_client.post("/auth/login", json=payload)
    
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_refresh_token(async_client: AsyncClient):
    payload = {"username": "test_user", "password": "superpassword"}
    await async_client.post("/auth/register", json=payload)
    login_res = await async_client.post("/auth/login", json=payload)
    refresh_token = login_res.json()["refresh_token"]

    response = await async_client.post("/auth/refresh", json={"refresh_token": refresh_token})
    
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_books_access_denied_without_token(async_client: AsyncClient):
    response = await async_client.get("/books/")

    assert response.status_code == 401 

@pytest.mark.asyncio
async def test_books_access_granted_with_token(async_client: AsyncClient):
    payload = {"username": "test_user", "password": "superpassword"}
    await async_client.post("/auth/register", json=payload)
    login_res = await async_client.post("/auth/login", json=payload)

    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get("/books/", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)