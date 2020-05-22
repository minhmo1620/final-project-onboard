import pytest

from app import create_app, db


@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    client = app.test_client()

    with app.app_context():
        from app.controllers.items import items_blueprint
        from app.controllers.categories import categories_blueprint
        from app.controllers.users import users_blueprint

        app.register_blueprint(categories_blueprint, url_prefix="/")
        app.register_blueprint(items_blueprint, url_prefix="/")
        app.register_blueprint(users_blueprint, url_prefix="/")

        db.drop_all()
        db.create_all()

        yield client  # this is where the testing happens!
