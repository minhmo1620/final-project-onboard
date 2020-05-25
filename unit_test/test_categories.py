from flask import json


def test_get_categories(client):
    """
    Test: Get all categories in the catalog
    "/categories"
    """
    response = client.get('/categories')
    assert response.status_code == 200
    assert [] == json.loads(response.data)


def test_create_category_success(client):
    """
    Test: Create a new category
    POST "/categories"
    """

    # create a new category
    data = {"name": "mia", "description": "abc"}
    response = client.post('/categories', json=data)
    assert response.status_code == 201
    assert {"message": "Created category successfully"} == json.loads(response.data)


# def test_create_category_fail(client):
    # existing category
    data = {"name": "mia", "description": "abc"}
    response = client.post('/categories', json=data)
    assert response.status_code == 400
    assert {"message": "Existed category"} == json.loads(response.data)

    # invalid input
    data = {"name": 123, "description": "abc"}
    response = client.post('/categories', json=data)
    assert response.status_code == 400
    assert {"name": ["Not a valid string."]} == json.loads(response.data)

    data = {"name": "mia", "description": 123}
    response = client.post('/categories', json=data)
    assert response.status_code == 400
    assert {"description": ["Not a valid string."]} == json.loads(response.data)

    data = {"name": "", "description": "abc"}
    response = client.post('/categories', json=data)
    assert response.status_code == 400
    assert {"name": ["Length must be between 1 and 100."]} == json.loads(response.data)
