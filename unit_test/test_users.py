import os
import pytest

from app import app, db, create_app


@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client  # this is where the testing happens!
    ctx.pop()


def test_create_user(client):
    data = {"username": "mia", "password": "abc"}
    rv = client.post('/users', json=data)
    assert rv.status_code == 201


def test_auth(client):
    data = {"username": "mia", "password": "abc"}
    rv = client.post('/auth', json=data)
    assert rv.status_code == 200

    data = {"username": "mia", "password": "abcd"}
    rv = client.post('/auth', json=data)
    assert rv.status_code == 401

