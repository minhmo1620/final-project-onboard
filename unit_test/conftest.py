import pytest

from app import create_app, db


@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    client = app.test_client()

    with app.app_context():
        from app.controller.items import items
        from app.controller.categories import categories
        from app.controller.users import users

        app.register_blueprint(categories, url_prefix="/")
        app.register_blueprint(items, url_prefix="/")
        app.register_blueprint(users, url_prefix="/")

        db.drop_all()
        db.create_all()

        yield client  # this is where the testing happens!
