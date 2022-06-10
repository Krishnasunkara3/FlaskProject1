from flask import Flask
from flask_restful import Api
from Resources.resource import Student, SearchByName, Test, StudentLogin
from db import db
from datetime import timedelta
from flask_jwt_extended import JWTManager
from task import workers

def create_app(db_location):

    # Starting the flask
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/1"
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = db_location
    db.init_app(app)
    api = Api(app)
    app.config["JWT_SECRET_KEY"] = 'login'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

    # Instantiating jwt and app object from their classes
    jwt = JWTManager(app)
    celery = workers.celery
    workers.celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.Task = workers.ContextTask

    api.add_resource(Student, '/student/<string:StudentId>')
    api.add_resource(SearchByName, '/student1/<string:StudentName>')
    api.add_resource(Test, '/test')
    api.add_resource(StudentLogin, '/login/<string:StudentName>')
    return app,celery


app,celery = create_app("postgresql://postgres:123@localhost:5432/Flask")
if __name__ == "__main__":

    app.run(debug=True)
