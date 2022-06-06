from db import db

# Creating student model
class StudentModel(db.Model):
    __tablename__ = "students"
    StudentId = db.Column(db.Integer, primary_key=True)
    StudentName = db.Column(db.String(100), nullable=False)
    StudentClass = db.Column(db.String(50), nullable=False)
    StudentAge = db.Column(db.Integer, nullable=False)
    StudentAddress = db.Column(db.String(100))
    def __init__(self, StudentId, StudentName, StudentClass, StudentAge, StudentAddress):
        self.StudentId = StudentId
        self.StudentName = StudentName
        self.StudentClass = StudentClass
        self.StudentAge = StudentAge
        self.StudentAddress = StudentAddress

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def change_in_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


