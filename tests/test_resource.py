from flask import Flask
import json
from Resources.resource import Student


# def test_get_test(client):
#     response = client.get('/test')
#     print(response)
#     assert response.status_code == 201
#     assert response.content_type == "application/json"



def test_get(client):

    response = client.get('/student/103')
    print(response.data)
    assert response.status_code == 200
    assert response.json['StudentId'] == 103
    assert response.json['StudentName'] == 'Raju'


def test_get_stuname(client):

    response = client.get('/student1/Raju')
    assert response.status_code == 200

def test_post(client):
    pay_out = {
        "StudentId": 106,
        "StudentName": "krishna",
        "StudentClass": "8th",
        "StudentAge": 15,
        "StudentAddress": "Korumilli"
    }
    resource = client.post('/student/106', json=pay_out)
    assert resource.status_code == 201


def test_put(client):
    pay_out = {
        "StudentName": "Tripura"
    }
    resource = client.put('/student/106', json=pay_out)
    assert resource.status_code == 200

def test_delete(client):

    resource = client.delete('/student/106')
    assert resource.status_code == 204



# def test_get_stuname(client):
#     response = client.get('/student1/krishna')
#     print(response.data)


