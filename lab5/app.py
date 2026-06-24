from flask import Flask, redirect
from flask_restful import Api
from flasgger import Swagger
from core.database import init_db

from api.resources import BookListResource, BookResource

app = Flask(__name__)
api = Api(app)

swagger = Swagger(app, template={
    "info": {
        "title": "Library Flask API",
        "description": "API бібліотеки, написане на Flask-RESTful",
        "version": "1.0.0"
    }
})

@app.route("/")
def root():
    return redirect("/apidocs/")

with app.app_context():
    init_db()

api.add_resource(BookListResource, '/books/')
api.add_resource(BookResource, '/books/<string:book_id>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)