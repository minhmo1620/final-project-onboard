from flask import json

from unit_test.helpers import create_headers, create_dummy_category, create_dummy_user, create_item


def test_create_item(client):
    """
    A test for creating a new item
    post('/categories/1/items')
    """
    # create header
    token1 = create_dummy_user(username="mia", password="abc")
    headers = create_headers(token1)
    create_dummy_category(name="category", description="description")

    # invalid input
    data1 = {"name": 3, "description": "abc"}
    response = client.post('/categories/1/items', json=data1, headers=headers)
    assert response.status_code == 400
    assert {"name": ["Not a valid string."]} == json.loads(response.data)

    # create a new item
    data2 = {"name": "category", "description": "description"}
    response = client.post('/categories/1/items', json=data2, headers=headers)
    assert response.status_code == 201
    assert {"message": "Created item successfully"} == json.loads(response.data)

    # existing item
    data3 = {"name": "category", "description": "description"}
    response = client.post('/categories/1/items', json=data3, headers=headers)
    assert response.status_code == 400
    assert {"message": "Existed item"} == json.loads(response.data)


def test_get_items(client):
    """
    Test: Get all items of one category
    GET ('/categories/1/items')
    """
    create_dummy_user(username="mia", password="abc")
    create_dummy_category(name="name", description="description")

    # create a get request to take all items from category 1
    # the id of this item is 1
    response = client.get('categories/1/items', json={})
    assert response.status_code == 200
    assert [] == json.loads(response.data)

    create_item(name="item", description="description")
    response = client.get('categories/1/items', json={})
    assert response.status_code == 200
    expected_result = [{"name": "item", "description": "description"}]
    assert expected_result == json.loads(response.data)


def test_get_item(client):
    """
    Test: Get one specific item
    """
    token1 = create_dummy_user(username="mia", password="abc")
    create_dummy_category(name="category", description="description")
    create_item(name="item", description="description")

    # create a get request for item 1
    response = client.get('categories/1/items/1', json={})
    assert response.status_code == 200
    expected_result = {"name": "item", "description": "description"}
    assert expected_result == json.loads(response.data)

    # try to get not existing item
    response = client.get('categories/1/items/2', json={})
    assert response.status_code == 404
    expected_result = {"message": "Item not found"}
    assert expected_result == json.loads(response.data)


def test_edit_item(client):
    """
    Test: Edit a specific item
    put ('/categories/1/items')
    """
    # create a new header
    token = create_dummy_user(username="mia", password="abc")
    header1 = create_headers(token)
    create_dummy_category(name="category", description="description")
    create_item(name="item", description="description")

    # invalid input
    data1 = {"description": 1}
    response = client.put('/categories/1/items/1', json=data1, headers=header1)
    assert response.status_code == 400
    assert {"description": ["Not a valid string."]} == json.loads(response.data)

    # update successfully
    data2 = {"description": "new description"}
    response = client.put('/categories/1/items/1', json=data2, headers=header1)
    assert response.status_code == 200
    expected_result = {"description": "new description", "name": "item"}
    assert expected_result == json.loads(response.data)

    # item not found
    data2 = {"description": "new description"}
    response = client.put('/categories/1/items/2', json=data2, headers=header1)
    assert response.status_code == 404
    expected_result = {"message": "Item not found"}
    assert expected_result == json.loads(response.data)

    # unauthenticated account
    token2 = create_dummy_user(username="abc", password="mia")
    header2 = create_headers(token2)
    response = client.put('/categories/1/items/1', json=data2, headers=header2)
    assert response.status_code == 403
    expected_result = {"message": "Unauthorized"}
    assert expected_result == json.loads(response.data)


def test_delete_item(client):
    """
    Test: Delete one specific item
    delete ('/categories/1/items/1')
    """
    # create headers for request (wrong password) -> Unauthorized
    token = create_dummy_user(username="mia", password="abc")
    header1 = create_headers(token)
    create_dummy_category(name="category", description="description")
    create_item(name="item", description="description")

    token1 = create_dummy_user(username="abc", password="mia")
    header2 = create_headers(token1)
    response = client.delete('/categories/1/items/1', json={}, headers=header2)
    assert response.status_code == 403
    expected_result = {"message": "Unauthorized"}
    assert expected_result == json.loads(response.data)

    # authorized but item not found
    response = client.delete('/categories/1/items/2', json={}, headers=header1)
    assert response.status_code == 404
    expected_result = {"message": "Item not found"}
    assert expected_result == json.loads(response.data)

    # authorized and delete successfully
    header3 = create_headers(token)
    response = client.delete('/categories/1/items/1', json={}, headers=header1)
    assert response.status_code == 200
    expected_result = {"message": "Deleted item successfully"}
    assert expected_result == json.loads(response.data)
