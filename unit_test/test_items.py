from unit_test.helpers import create_headers, create_category, create_dummy_user, create_item


def test_create_item(client):
    """
    A test for creating a new item
    post('/categories/1/items')
    """
    # create header
    token = create_dummy_user(username="mia", password="abc")
    headers = create_headers(username="mia", password="abc")
    create_category(name="category", description="description")

    # invalid input
    data1 = {"name": 3, "description": "abc"}
    response = client.post('/categories/1/items', json=data1, headers=headers)
    assert response.status_code == 400

    # create a new item
    data2 = {"name": "category", "description": "description"}
    response = client.post('/categories/1/items', json=data2, headers=headers)
    assert response.status_code == 201

    # existing item
    data3 = {"name": "category", "description": "description"}
    response = client.post('/categories/1/items', json=data3, headers=headers)
    assert response.status_code == 400


def test_get_items(client):
    """
    Test: Get all items of one category
    GET ('/categories/1/items')
    """
    create_category(name="name", description="description")

    # create a get request to take all items from category 1
    # the id of this item is 1
    rv = client.get('categories/1/items', json={})
    assert rv.status_code == 200


def test_get_item(client):
    """
    Test: Get one specific item
    """
    create_dummy_user(username="mia", password="abc")
    create_category(name="name", description="description")
    create_item(name="item", description="description")

    # create a get request for item 1
    rv = client.get('categories/1/items/1', json={})
    assert rv.status_code == 200

    # try to get not existing item
    rv = client.get('categories/1/items/2', json={})
    assert rv.status_code == 404


def test_edit_item(client):
    """
    Test: Edit a specific item
    put ('/categories/1/items')
    """
    # create a new header
    token = create_dummy_user(username="mia", password="abc")
    header1 = create_headers(username="mia", password="abc")
    create_category(name="category", description="description")
    create_item(name="item", description="description")

    # invalid input
    data1 = {"description": 1}
    rv = client.put('/categories/1/items/1', json=data1, headers=header1)
    assert rv.status_code == 400

    # update successfully
    data2 = {"description": "new description"}
    rv = client.put('/categories/1/items/1', json=data2, headers=header1)
    assert rv.status_code == 200

    # item not found
    data2 = {"description": "new description"}
    rv = client.put('/categories/1/items/2', json=data2, headers=header1)
    assert rv.status_code == 404

    # unauthorized account
    # header2 = create_headers(username="mia", password="abcd")
    # rv = client.put('/categories/1/items/1', json=data2, headers=header2)
    # assert rv.status_code == 401


def test_delete_item(client):
    """
    Test: Delete one specific item
    delete ('/categories/1/items/1')
    """
    # create headers for request (wrong password) -> Unauthorized
    token = create_dummy_user(username="mia", password="abc")
    header1 = create_headers(username="mia", password="abc")
    create_category(name="category", description="description")
    create_item(name="item", description="description")

    # rv = client.delete('/categories/1/items/1', json={}, headers=header1)
    # assert rv.status_code == 401

    # authorized but item not found
    # header2 = create_headers(token)
    rv = client.delete('/categories/1/items/2', json={}, headers=header1)
    assert rv.status_code == 404

    # authorized and delete successfully
    header3 = create_headers("mia", "abc")
    rv = client.delete('/categories/1/items/1', json={}, headers=header1)
    assert rv.status_code == 200
