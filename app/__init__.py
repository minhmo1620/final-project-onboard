import os
from flask import Flask, Blueprint
from .helpers import authenticate, identity

from .db import db
from .models.users import UserModel
from .models.items import ItemModel
from .models.categories import CategoryModel


def create_app(env):

    env = {'test':'app.config.staging.TestingConfig',
           'development':'app.config.development.DevelopConfig',
           'local': 'app.config.staging.TestingConfig',
           'production':'app.config.staging.TestingConfig'}
    app = Flask(__name__)
    app.config.from_object('app.config.staging.TestingConfig')
    db.init_app(app)

    with app.app_context():
        from .controller.items import items
        from .controller.categories import categories
        from .controller.users import users

        app.register_blueprint(categories, url_prefix="/")
        app.register_blueprint(items, url_prefix="/")
        app.register_blueprint(users, url_prefix="/")

        db.create_all()

    return app


app = create_app()
app.app_context().push()









