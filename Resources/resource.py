from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models.model import StudentModel


student_args = reqparse.RequestParser()
student_args.add_argument("StudentId", type=int, help="Student id is required", required=True)
student_args.add_argument("StudentName", type=str, help="Student name is required", required=True)
student_args.add_argument("StudentClass", type=str, help="Student name is required", required=True)
student_args.add_argument("StudentAge", type=int, help="Student id is required", required=True)
student_args.add_argument("StudentAddress", type=str, required=False)

student_put_args = reqparse.RequestParser()
student_put_args.add_argument("StudentId", type=int, help="Student id is required")
student_put_args.add_argument("StudentName", type=str, help="Student name is required")
student_put_args.add_argument("StudentClass", type=str, help="Student name is required")
student_put_args.add_argument("StudentAge", type=int, help="Student id is required")
student_put_args.add_argument("StudentAddress", type=str)

resource_fields = {
                        'StudentId': fields.Integer,
                        'StudentName': fields.String,
                        'StudentClass': fields.String,
                        'StudentAge': fields.Integer,
                        'StudentAddress': fields.String
                 }


class Student(Resource):
    @marshal_with(resource_fields)
    def get(self, StudentId):
        result = StudentModel.query.filter_by(StudentId=StudentId).first()
        if not result:
            abort(404, message="student id not available")
        return result, 200

    @marshal_with(resource_fields)
    def post(self, StudentId):
        args = student_args.parse_args()
        result = StudentModel.query.filter_by(StudentId=StudentId).first()
        if result:
            abort(404, message="student id  is already available")

        student_details = StudentModel(StudentId=StudentId, StudentName=args["StudentName"],
                                       StudentClass=args["StudentClass"], StudentAge=args["StudentAge"],
                                       StudentAddress=args["StudentAddress"])
        student_details.save_to_db()
        return student_details, 201

    @marshal_with(resource_fields)
    def put(self, StudentId):
        args = student_put_args.parse_args()
        result = StudentModel.query.filter_by(StudentId=StudentId).first()

        if not result:
            abort(404, message="student id not available")

        if args["StudentName"]:
            result.StudentName = args["StudentName"]

        if args["StudentClass"]:
            result.StudentClass = args["StudentClass"]

        if args["StudentAge"]:
            result.StudentAge = args["StudentAge"]

        if args["StudentAddress"]:
            result.StudentAddress = args["StudentAddress"]

        result.change_in_db()

        return result

    def delete(self, StudentId):
        result = StudentModel.query.filter_by(StudentId=StudentId).first()
        if not result:
            abort(404, message="student id not available")

        result.delete_from_db()

        return {StudentId: 'student id is deleted'}, 204


class SearchByName(Resource):
    @marshal_with(resource_fields)
    def get(self, StudentName):
        result = StudentModel.query.filter_by(StudentName=StudentName).all()
        if not result:
            abort(404, message="student name not available")
        return result

class Test(Resource):

    def get(self):
        return {'hello':'world'}, 201