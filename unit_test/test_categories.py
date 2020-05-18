import os
import pytest
import tempfile

from app import app, db

@pytest.fixture
def client():
    db_fd, url = tempfile.mkstemp()
    url = 'sqlite://'+ url
    app.config['DATABASE_URI'] = url
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE_URI'])


def test_get_categories(client):
    rv = client.get('/categories')
