import jwt

from app import app
from app.models.users import UserModel
from app.models.categories import CategoryModel
from app.models.items import ItemModel
from app.helpers import hash_password, create_salt
from app.db import db

secret_key = app.config["SECRET_KEY"]


def create_dummy_user(username, password):
    user = db.session.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        salt = create_salt()
        hashed_password = hash_password(password + salt)

        new_user = UserModel(username, hashed_password, salt)

        token = jwt.encode({'user': username}, secret_key).decode('UTF-8')

        db.session.add(new_user)
        db.session.commit()

        return token
    if user.password != hash_password(password + user.salt):
        return 401
    return jwt.encode({"user": username}, secret_key).decode('UTF-8')


def create_category(name, description):
    """
    This test is to create a new category in the database to test other functions for item (get, put, post, delete)
    """

    # create data for request
    data = {"name": name, "description": description}

    new_category = CategoryModel(name=name, description=description)

    db.session.add(new_category)
    db.session.commit()


def create_headers(username, password):
    """
    This function will create headers for the request and will be called in other tests
    Normally, this function will be used to take the token from username and password to authenticate

    Input:
        - username
        - password
    Output: header
    """
    # data type in the body
    body_type = 'application/json'

    # take the token
    user = db.session.query(UserModel).filter(UserModel.username == username).first()

    if not user:
        return 404
    if user.password != hash_password(password + user.salt):
        return 401

    token = jwt.encode({'user': username}, secret_key).decode('UTF-8')

    # create header
    headers = {
        'Content-Type': body_type,
        'Authorization': "Bearer " + token
    }
    return headers


def create_item(name, description):
    category_id = 1
    user_id = 1

    new_item = ItemModel(name=name,
                         description=description,
                         user_id=user_id,
                         category_id=category_id)
    db.session.add(new_item)
    db.session.commit()
