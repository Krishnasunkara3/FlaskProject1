from flask import Flask
from flask_restful import Api
from Resources.resource import Student, SearchByName, Test
from db import db

def create_app(db_location):

    # Starting the flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = db_location
    db.init_app(app)
    api = Api(app)
    api.add_resource(Student, '/student/<string:StudentId>')
    api.add_resource(SearchByName, '/student1/<string:StudentName>')
    api.add_resource(Test, '/test')
    return app


if __name__ == "__main__":
    app = create_app("postgresql://postgres:123@localhost:5432/Flask")
    app.run(host='0.0.0.0', port=6001, debug=True)
