from .helpers import client


def test_create_user(client):
    data = {"username": 230, "password": "abc"}
    rv = client.post('/users', json=data)
    assert rv.status_code == 422

    data = {"username": "mia", "password": "abc"}
    rv = client.post('/users', json=data)
    assert rv.status_code == 201

    data = {"username": "mia", "password": ""}
    rv = client.post('/users', json=data)
    assert rv.status_code == 400


def test_auth(client):
    data = {"username": "mia", "password": "abc"}
    rv = client.post('/auth', json=data)
    assert rv.status_code == 200

    data = {"username": "mia", "password": "abcd"}
    rv = client.post('/auth', json=data)
    assert rv.status_code == 401

