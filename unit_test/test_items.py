from .helpers import client


def test_create_category(client):
    data = {"name": "mia", "description": "abc"}
    rv = client.post('/categories', json=data)

    return rv


def user(client, username, password):
    data1 = {"username": username, "password": password}

    rps = client.post('/users', json=data1)
    if rps.status_code == 400:
        rps = client.post('/auth', json=data1)

    if rps.status_code == 401:
        return 401

    if rps.status_code == 422:
        return 422

    data = rps.get_json()
    token = str(data['access_token'])

    return token


def headers(client, username, password):
    mimetype = 'application/json'
    token = user(client, username, password)
    header = {
        'Content-Type': mimetype,
        'Authorization': token
    }
    return header


def test_create_item(client):
    header = headers(client, "mia", "abc")
    data1 = {"name": 3, "description": "abc"}
    rv = client.post('/categories/1/items', json=data1, headers=header)
    assert rv.status_code == 422

    data2 = {"name": "category", "description": "description"}
    rv = client.post('/categories/1/items', json=data2, headers=header)
    assert rv.status_code == 201

    data3 = {"name": "category", "description": "description"}
    rv = client.post('/categories/1/items', json=data3, headers=header)
    assert rv.status_code == 400


def test_get_items(client):
    rv = client.get('categories/1/items', json={})
    assert rv.status_code == 200


def test_get_item(client):
    rv = client.get('categories/1/items/1', json={})
    assert rv.status_code == 200

    rv = client.get('categories/1/items/2', json={})
    assert rv.status_code == 404


def test_edit_item(client):
    header1 = headers(client, "mia", "abc")

    data1 = {"description": (1, 2, 3)}
    rv = client.post('/categories/1/items', json=data1, headers=header1)
    assert rv.status_code == 422

    data2 = {"description": "new description"}
    rv = client.put('/categories/1/items/1', json=data2, headers=header1)
    assert rv.status_code == 200

    header2 = headers(client, "mia", "abcd")
    rv = client.put('/categories/1/items/1', json=data2, headers=header2)
    assert rv.status_code == 401


def test_delete_item(client):
    header1 = headers(client, "mia", "abcd")
    rv = client.delete('/categories/1/items/1', json={}, headers=header1)
    assert rv.status_code == 401

    header2 = headers(client, "mia", "abc")
    rv = client.delete('/categories/1/items/2', json={}, headers=header2)
    assert rv.status_code == 404

    header3 = headers(client, "mia", "abc")
    rv = client.delete('/categories/1/items/1', json={}, headers=header3)
    assert rv.status_code == 200


