from .helpers import client


def test_create_user(client):
    data = {"username": "mia", "password": "abc"}
    rv = client.post('/users', json=data)
    assert rv.status_code == 201


def test_auth(client):
    data = {"username": "mia", "password": "abc"}
    rv = client.post('/auth', json=data)
    rv = client.post('/auth', json=data)
    assert rv.status_code == 200

    data = {"username": "mia", "password": "abcd"}
    rv = client.post('/auth', json=data)
    assert rv.status_code == 401

