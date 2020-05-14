from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Resource
from flask_jwt import JWT

from .securtity import authenticate, identity
from .models.users import UserModel
from .models.items import ItemModel
from .models.categories import CategoryModel

# from app import app
#
# from .controller import items
# from .controller import categories
# from .controller import auth
#
# app.register_blueprint(auth, url_prefix="/")
# app.register_blueprint(categories, url_prefix="/categories")
# app.register_blueprint(items, url_prefix="/categories/<int: category_id>/items")




