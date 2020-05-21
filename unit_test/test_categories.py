def test_get_categories(client):
    """
    Test: Get all categories in the catalog
    """
    rv = client.get('/categories')
    assert rv.status_code == 200


def test_create_category(client):
    """
    Test: Create a new category
    """

    # create a new category
    data = {"name": "mia", "description": "abc"}
    rv = client.post('/categories', json=data)
    assert rv.status_code == 201

    # existing category
    rsp = client.post('/categories', json=data)
    assert rsp.status_code == 400

    # invalid input
    data = {"name": 123, "description": "abc"}
    rv = client.post('/categories', json=data)
    assert rv.status_code == 422

    data = {"name": "mia", "description": 123}
    rv = client.post('/categories', json=data)
    assert rv.status_code == 422
