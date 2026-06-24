import pytest
import mongomock

from app import app
from core.database import db

@pytest.fixture(autouse=True)
def setup_db():
    """
    Автоматично підміняє реальне підключення на базу в оперативній пам'яті (mongomock)
    перед кожним тестом, і очищає її після.
    """
    db.client = mongomock.MongoClient()
    yield
    db.client.drop_database('books')

@pytest.fixture
def client():
    """Створює клієнт для імітації запитів до нашого Flask API"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_book(client):
    payload = {
        "title": "Flask Book", 
        "author": "Test Author", 
        "description": "Test Description", 
        "status": "available", 
        "year": 2024
    }

    response = client.post("/books/", json=payload)
    
    assert response.status_code == 201

    data = response.get_json()
    assert data["title"] == payload["title"]

def test_pagination_limit_offset(client):
    for i in range(3):
        payload = {
            "title": f"Book {i}", 
            "author": "A", 
            "description": "D", 
            "status": "available", 
            "year": 2000
        }
        client.post("/books/", json=payload)

    response_1 = client.get("/books/?limit=2&offset=0")
    assert response_1.status_code == 200
    data_1 = response_1.get_json()
    
    assert len(data_1) == 2
    assert data_1[0]["title"] == "Book 0"
    assert data_1[1]["title"] == "Book 1"

    response_2 = client.get("/books/?limit=2&offset=2")
    assert response_2.status_code == 200
    data_2 = response_2.get_json()
    
    assert len(data_2) == 1 
    assert data_2[0]["title"] == "Book 2"