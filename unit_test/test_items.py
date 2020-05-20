from .helpers import client


def test_create_category(client):
    data = {"name": "mia", "description": "abc"}
    rv = client.post('/categories', json=data)


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
    header = {
        'Content-Type': mimetype,
        'Authorization': token
    }
    return header


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
