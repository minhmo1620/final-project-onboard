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


def test_get_categories(client):
    rv = client.get('/categories')
    assert rv.status_code == 200


def test_create_category(client):
    data = {"name": "mia", "description": "abc"}
    rv = client.post('/categories', json=data)
    assert rv.status_code == 201

    rsp = client.post('/categories', json=data)
    assert rsp.status_code == 400
