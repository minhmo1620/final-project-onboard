from .helpers import client


def test_get_categories(client):
    rv = client.get('/categories')
    assert rv.status_code == 200


def test_create_category(client):
    data = {"name": "mia", "description": "abc"}
    rv = client.post('/categories', json=data)
    assert rv.status_code == 201

    rsp = client.post('/categories', json=data)
    assert rsp.status_code == 400
