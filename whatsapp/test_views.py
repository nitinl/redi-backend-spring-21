import pytest
import os
from app import app, db
import models


@pytest.fixture
def client():
    """
    Create a temporary db with some data in it for using in the tests.
    """
    app.config["TESTING"] = True
    app.testing = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        user1 = models.User(username='tom', phone_number='8913748123')
        user2 = models.User(username='harry', phone_number='88349572345')
        message = models.Message(text='hi', sender=1, receiver=2)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(message)
        db.session.commit()
    yield client

    os.remove('test.db')


def test_send_message(client):
    response = client.post("/send_message", json={"sender": 1, "receiver": 2, "message": "we'll learn testing today."})
    assert response.json == {"response": "OK"}
    message_in_db = models.Message.query.filter_by(sender=1, receiver=2).order_by(
        models.Message.timestamp.desc()).first()
    assert message_in_db.text == "we'll learn testing today."


def test_update_message(client):
    response = client.put("/update_message", json={"sender": 1, "receiver": 2, "message": "hello"})
    assert response.json == {"response": "OK"}
    message_in_db = models.Message.query.filter_by(sender=1, receiver=2).order_by(
        models.Message.timestamp.desc()).first()
    assert message_in_db.text == 'hello'
