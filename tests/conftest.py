from flask import Flask
import pytest
from app import create_app


@pytest.fixture(scope="session")
def client():

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    app = create_app("postgresql://postgres:123@localhost:5432/Flask")
    client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield client  # this is where the testing happens!

    ctx.pop()