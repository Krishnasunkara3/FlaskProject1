from flask import request,jsonify
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models.model import StudentModel
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from task.celery_task import update_date_time
from task.manage import manage_session


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
    @jwt_required()
    @marshal_with(resource_fields)
    @manage_session
    def get(self, StudentId):
        result = StudentModel.query.filter_by(StudentId=StudentId).first()
        if not result:
            abort(404, message="student id not available")

        update_date_time.apply_async(args=(StudentId), countdown=0.0001)
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
        # update_date_time.apply_async(StudentId)
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

        # update_date_time.apply_async(StudentId)
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

class StudentLogin(Resource):


    def post(self,StudentName):

        try:
         user = StudentModel.query.filter_by(StudentName=StudentName).first();
         if user:
          access_token = create_access_token(identity=StudentName)
          return jsonify(access_token=access_token);
         else:
            return {"msg":"Please check Student ","status":403},403
        except Exception as e:
            return {"status":500,"msg":str(e)}


class Test(Resource):

    def get(self):
        return {'hello':'world'}, 201