# import fixture function to run test
from .helpers import client


def test_create_user(client):
    """
    Test: Create a new user
    """

    # invalid input
    data = {"username": 230, "password": "abc"}
    rv = client.post('/users', json=data)
    assert rv.status_code == 422

    # create a new user
    data = {"username": "mia", "password": "abc"}
    rv = client.post('/users', json=data)
    assert rv.status_code == 201

    # existing user
    data = {"username": "mia", "password": ""}
    rv = client.post('/users', json=data)
    assert rv.status_code == 400


def test_auth(client):
    """
    Test: Authorization
    """

    # valid user
    data = {"username": "mia", "password": "abc"}
    rv = client.post('/auth', json=data)
    assert rv.status_code == 200

    # wrong password
    data = {"username": "mia", "password": "abcd"}
    rv = client.post('/auth', json=data)
    assert rv.status_code == 401

