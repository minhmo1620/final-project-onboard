import os

from flask_marshmallow import Marshmallow

from flask import Flask, Blueprint
from flask_jwt import JWT
from .helpers import authenticate, identity

from .db import db
from .models.users import UserModel
from .models.items import ItemModel
from .models.categories import CategoryModel

from .controller.items import items
from .controller.categories import categories


def create_app():

    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    db.init_app(app)

    with app.app_context():
        app.register_blueprint(categories, url_prefix="")
        app.register_blueprint(items, url_prefix="")

        db.create_all()

    jwt = JWT(app, authenticate, identity)

    return app


app = create_app()
app.app_context().push()
ma = Marshmallow(app)








