from task.workers import celery
from models.model import StudentModel
import datetime


@celery.task()
def update_date_time(student_id):
    print('inside celery task')
    result = StudentModel.query.filter_by(StudentId=student_id).first()
    result.updated_on = datetime.datetime.utcnow
    result.change_in_db()
    return "success"
