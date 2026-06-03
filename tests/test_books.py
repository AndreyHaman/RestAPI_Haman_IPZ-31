from fastapi.testclient import TestClient
from main import app
from models.data import books_db

client = TestClient(app)

def setup_function():
    # Очищаємо "БД" перед кожним тестом для чистоти експерименту
    books_db.clear()

def test_create_book():
    response = client.post("/books/", json={
        "title": "Тестова Книга",
        "author": "Тестовий Автор",
        "year": 2026,
        "status": "available"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестова Книга"
    assert "id" in data

def test_get_all_books():
    client.post("/books/", json={"title": "Книга 1", "author": "Автор 1", "year": 2020, "status": "available"})
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_delete_book_idempotent():
    # 1. Додаємо книгу
    create_res = client.post("/books/", json={"title": "Книга на видалення", "author": "Автор", "year": 2021, "status": "available"})
    book_id = create_res.json()["id"]

    # 2. Видаляємо вперше (повинно бути 204)
    del_res1 = client.delete(f"/books/{book_id}")
    assert del_res1.status_code == 204

    # 3. Видаляємо вдруге (все одно повинно бути 204 - перевірка на ідемпотентність)
    del_res2 = client.delete(f"/books/{book_id}")
    assert del_res2.status_code == 204

def test_get_book_not_found():
    response = client.get("/books/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404