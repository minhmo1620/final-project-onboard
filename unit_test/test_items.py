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

def user(client):
    data1 = {"username": "miso", "password": "abc"}

    rps = client.post('/users', json=data1)
    if rps.status_code == 400:
        rps = client.post('/auth', json=data1)

    data = rps.get_json()
    token = str(data['access_token'])

    return token


def headers(client):
    mimetype = 'application/json'
    token = user(client)
    headers = {
        'Content-Type': mimetype,
        'Authorization': token
    }
    return headers


def test_create_item(client):
    header = headers(client)
    data2 = {"name": "he", "description": "abc"}
    rv = client.post('/categories/1/items', json=data2, headers=header)
    assert rv.status_code == 201


def test_get_items(client):
    rv = client.get('categories/1/items', json={})

    assert rv.status_code == 200


def test_get_item(client):
    rv = client.get('categories/1/items/1', json={})

    assert rv.status_code == 200


def test_edit_item(client):
    header = headers(client)
    data2 = {"description": "new description"}
    rv = client.put('/categories/1/items/1', json=data2, headers=header)
    assert rv.status_code == 200


def test_delete_item(client):
    header = headers(client)
    data2 = {}
    rv = client.delete('/categories/1/items/1', json=data2, headers=header)
    assert rv.status_code == 200
