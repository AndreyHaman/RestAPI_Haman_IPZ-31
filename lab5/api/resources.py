from flask import request
from flask_restful import Resource
from schemas.book import BookCreate, BookResponse
from services.book_service import BookService
from core.database import get_database

def get_book_service():
    db = get_database()
    return BookService(db)

class BookListResource(Resource):
    def get(self):
        """
        Отримати список всіх книг з пагінацією
        ---
        tags:
          - Books
        parameters:
          - name: limit
            in: query
            type: integer
            required: false
            default: 10
          - name: offset
            in: query
            type: integer
            required: false
            default: 0
        responses:
          200:
            description: Успішно отримано список книг
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "65fd2ac8ecc52e049776c3c5"
                  title:
                    type: string
                    example: "1984"
                  author:
                    type: string
                    example: "Джордж Оруелл"
                  description:
                    type: string
                    example: "Класична antiutopia"
                  status:
                    type: string
                    example: "available"
                  year:
                    type: integer
                    example: 1949
        """
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        
        service = get_book_service()
        books = service.get_all_books(limit=limit, offset=offset)
        return [BookResponse(**book).model_dump(mode='json', by_alias=False) for book in books], 200

    def post(self):
        """
        Додати нову книгу
        ---
        tags:
          - Books
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - title
                - author
                - description
                - year
              properties:
                title:
                  type: string
                  example: "Кобзар"
                author:
                  type: string
                  example: "Тарас Шевченко"
                description:
                  type: string
                  example: "Збірка поетичних творів"
                status:
                  type: string
                  example: "available"
                year:
                  type: integer
                  example: 1840
        responses:
          201:
            description: Книгу успішно створено
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "65fd2ac8ecc52e049776c3c5"
                title:
                  type: string
                  example: "Кобзар"
                author:
                  type: string
                  example: "Тарас Шевченко"
                description:
                  type: string
                  example: "Збірка поетичних творів"
                status:
                  type: string
                  example: "available"
                year:
                  type: integer
                  example: 1840
          400:
            description: Помилка валідації даних
        """
        data = request.get_json()
        
        try:
            book_in = BookCreate(**data)
        except ValueError as e:
            return {"message": "Помилка валідації", "details": str(e)}, 400
        
        service = get_book_service()
        new_book = service.create_book(book_in)
        
        return BookResponse(**new_book).model_dump(mode='json', by_alias=False), 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за її ID
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
            description: Унікальний ідентифікатор книги
        responses:
          200:
            description: Дані книги успішно отримано
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "65fd2ac8ecc52e049776c3c5"
                title:
                  type: string
                  example: "1984"
                author:
                  type: string
                  example: "Джордж Оруелл"
                description:
                  type: string
                  example: "Класична антиутопія"
                status:
                  type: string
                  example: "available"
                year:
                  type: integer
                  example: 1949
          404:
            description: Книгу не знайдено
        """
        service = get_book_service()
        book = service.get_book_by_id(book_id)
        
        if book:
            return BookResponse(**book).model_dump(mode='json', by_alias=False), 200
        return {"message": "Книгу не знайдено"}, 404

    def delete(self, book_id):
        """
        Видалити книгу за її ID
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
            description: Унікальний ідентифікатор книги
        responses:
          204:
            description: Книгу успішно видалено
          404:
            description: Книгу не знайдено
        """
        service = get_book_service()
        deleted = service.delete_book(book_id)
        
        if deleted:
            return '', 204
        return {"message": "Книгу не знайдено"}, 404