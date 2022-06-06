from models.model import StudentModel

def test_new_user():

    user = StudentModel(110, 'krishna', '10th', 15, 'Korumilli')

    assert user.StudentId == 110
    assert user.StudentName == 'krishna'
    assert user.StudentClass == '10th'
    assert user.StudentAge == 15
    assert user.StudentAddress == 'Korumilli'