def test_create_category(client):
    """
    This test is to create a new category in the database to test other functions for item (get, put, post, delete)
    """

    # create data for request
    data = {"name": "mia", "description": "abc"}

    # create a request
    rv = client.post('/categories', json=data)

    return rv


def user(client, username, password):
    """
    This function will take username and password of user and return token
    """

    # data of user
    data1 = {"username": username, "password": password}

    # create request to create a new user or authenticate existing user
    rps = client.post('/users', json=data1)
    if rps.status_code == 400:
        rps = client.post('/auth', json=data1)

    # some corner cases
    if rps.status_code == 401:
        return 401

    if rps.status_code == 422:
        return 422

    # get the data from response of the above request
    data = rps.get_json()

    # get token
    token = str(data['access_token'])

    return token


def headers(client, username, password):
    """
    This function will create headers for the request and will be called in other tests
    Normally, this function will be used to take the token from username and password to authenticate

    Input:
        - username
        - password
    Output: header
    """
    # data type in the body
    body_type = 'application/json'

    # take the token
    token = user(client, username, password)

    # create header
    header = {
        'Content-Type': body_type,
        'Authorization': token
    }
    return header


def test_create_item(client):
    """
    A test for creating a new item
    post('/categories/1/items')
    """
    # create header
    header = headers(client, "mia", "abc")

    # invalid input
    data1 = {"name": 3, "description": "abc"}
    rv = client.post('/categories/1/items', json=data1, headers=header)
    assert rv.status_code == 422

    # create a new item
    data2 = {"name": "category", "description": "description"}
    rv = client.post('/categories/1/items', json=data2, headers=header)
    assert rv.status_code == 201

    # existing item
    data3 = {"name": "category", "description": "description"}
    rv = client.post('/categories/1/items', json=data3, headers=header)
    assert rv.status_code == 400


def test_get_items(client):
    """
    Test: Get all items of one category
    GET ('/categories/1/items')
    """

    # create a get request to take all items from category 1
    # the id of this item is 1
    rv = client.get('categories/1/items', json={})
    assert rv.status_code == 200


def test_get_item(client):
    """
    Test: Get one specific item
    """
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
    header1 = headers(client, "mia", "abc")

    # invalid input
    data1 = {"description": 1}
    rv = client.put('/categories/1/items/1', json=data1, headers=header1)
    assert rv.status_code == 422

    # update successfully
    data2 = {"description": "new description"}
    rv = client.put('/categories/1/items/1', json=data2, headers=header1)
    assert rv.status_code == 200

    # item not found
    data2 = {"description": "new description"}
    rv = client.put('/categories/1/items/2', json=data2, headers=header1)
    assert rv.status_code == 404

    # unauthorized account
    header2 = headers(client, "mia", "abcd")
    rv = client.put('/categories/1/items/1', json=data2, headers=header2)
    assert rv.status_code == 401


def test_delete_item(client):
    """
    Test: Delete one specific item
    delete ('/categories/1/items/1')
    """
    # create headers for request (wrong password) -> Unauthorized
    header1 = headers(client, "mia", "abcd")
    rv = client.delete('/categories/1/items/1', json={}, headers=header1)
    assert rv.status_code == 401

    # authorized but item not found
    header2 = headers(client, "mia", "abc")
    rv = client.delete('/categories/1/items/2', json={}, headers=header2)
    assert rv.status_code == 404

    # authorized and delete successfully
    header3 = headers(client, "mia", "abc")
    rv = client.delete('/categories/1/items/1', json={}, headers=header3)
    assert rv.status_code == 200
