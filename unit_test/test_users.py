from unit_test.helpers import create_dummy_user


def test_create_user(client):
    """
    Test: Create a new user, "/users"
    """

    # invalid input
    data = {"username": 230, "password": "abc"}
    response = client.post('/users', json=data)
    assert response.status_code == 400

    # create a new user
    data = {"username": "mia", "password": "abc"}
    response = client.post("/users", json=data)
    assert response.status_code == 201

    # existing user
    data = {"username": "mia", "password": ""}
    response = client.post("/users", json=data)
    assert response.status_code == 400


def test_auth(client):
    """
    Test: Authorization, "/auth"
    """
    create_dummy_user(username="mia", password="abc")

    # valid user
    data = {"username": "mia", "password": "abc"}
    response = client.post("/auth", json=data)
    assert response.status_code == 200

    # wrong password
    data = {"username": "mia", "password": "abcd"}
    response = client.post("/auth", json=data)
    assert response.status_code == 401
