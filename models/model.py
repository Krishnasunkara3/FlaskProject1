from db import db
import datetime

# Creating student model
class StudentModel(db.Model):
    __tablename__ = "students"
    StudentId = db.Column(db.Integer, primary_key=True)
    StudentName = db.Column(db.String(100), nullable=False)
    StudentClass = db.Column(db.String(50), nullable=False)
    StudentAge = db.Column(db.Integer, nullable=False)
    StudentAddress = db.Column(db.String(100))
    updated_on = db.Column(db.DateTime);
    def __init__(self, StudentId, StudentName, StudentClass, StudentAge, StudentAddress, updated_on):
        self.StudentId = StudentId
        self.StudentName = StudentName
        self.StudentClass = StudentClass
        self.StudentAge = StudentAge
        self.StudentAddress = StudentAddress
        self.updated_on = updated_on
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def change_in_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def find_by_username(self, StudentName):
        try:
            return db.query.filter_by(StudentName=StudentName).first();
        except Exception as e:
            print(e);

    # Function to check user identity
    @classmethod
    def find_by_id(cls, StudentId):
        try:
            return cls.query.filter_by(StudentId=StudentId).first();
        except Exception as e:
            print(e);


