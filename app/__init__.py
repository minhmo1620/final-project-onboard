import os
# import yaml

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from flask_mysqldb import MySQL
import mysql.connector
from .securtity import authenticate, identity

from .db import db
from .models.users import UserModel
from .models.items import ItemModel
from .models.categories import CategoryModel

from .controller.items import items
from .controller.categories import categories
from .controller.auth import auth


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    db.init_app(app)

    with app.app_context():
        app.register_blueprint(auth, url_prefix="")
        app.register_blueprint(categories, url_prefix="/categories")
        app.register_blueprint(items, url_prefix="/categories/<int:category_id>/items")

        db.create_all()

    jwt = JWT(app, authenticate, identity)

    return app


app = create_app()
app.app_context().push()









