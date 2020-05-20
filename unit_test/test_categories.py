import os
import pytest
import tempfile
import json

from app import app, db, create_app
app.config['TESTING'] = True

# @pytest.fixture
# def client():
#     db_fd, url = tempfile.mkstemp()
#     url = 'sqlite://' + url
#     app.config.from_object('app.config.staging.TestingConfig')
#     app.config['TESTING'] = True
#     client = app.test_client()
#     yield client
#     os.close(db_fd)
#     os.unlink(app.config.from_object('app.config.staging.TestingConfig'))


@pytest.fixture(scope='module')
def client():
    app = create_app()
    app.config.from_object('app.config.staging.TestingConfig')
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client  # this is where the testing happens!
    ctx.pop()


def test_get_categories(client):
    rv = client.get('/categories')
    assert rv.status_code == 200


def test_create_category(client):
    data = {"name": "hello", "description": "abc"}
    rv = client.post('/categories', json=data)
    assert rv.status_code == 201

    rsp = client.post('/categories', json=data)
    assert rsp.status_code == 400

# def test_create_category_fail(client):
#     data = {"name": "food", "description": "abc"}
#     client.post('/categories', json=data)
#
#     rv = client.post('/categories', json=data)
#
#     assert rv.status_code == 400
