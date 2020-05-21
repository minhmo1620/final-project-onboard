import os
import random
import jwt
from marshmallow import ValidationError
from flask import Blueprint, request, jsonify
from functools import wraps

from app import db
from ..helpers import hash_password
from ..models.users import UserModel, UserSchema

# create blueprint
users = Blueprint('users', __name__)

# take secret key from .env
secret_key = str(os.getenv('SECRET_KEY'))


def create_salt():
    """
    Create a random salt with 16 characters long
    """
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range(16):
        chars.append(random.choice(characters))
    return "".join(chars)


def token_required(f):
    """
    Decorator to validate the token and return user_id
    """

    @wraps(f)
    def decorator(*arg, **kwargs):
        token = request.headers["Authorization"].split()
        if token[0] != "Bearer":
            return jsonify({"message": "Invalid token"}), 401
        else:
            try:
                data = jwt.decode(token[1], secret_key)
                username = data['user']
                user = UserModel.find_by_username(username)
            except:
                return jsonify({'message': 'Token is invalid'}), 401
        return f(*arg, **kwargs, user_id=user.id)

    return decorator


# check the decorator
@users.route('/check', methods=['POST'])
@token_required
def check(user_id):
    data = request.headers
    print(data["Authorization"].split())
    return jsonify({})


@users.route('/users', methods=['POST'])
def create_user():
    """
    input:
        - username: string
        - password: string
    output:
        - raise error if username is existed
        - if username is not existed
            - create new salt
            - hash password
            --> create new user (username, hashed password, salt)
    """
    # take data from request
    data = request.get_json()

    # validate input
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    # information - username & password
    username = data['username']
    password = data['password']

    # check the existent of user
    if UserModel.find_by_username(username):
        return jsonify({'message': 'existed username'}), 400

    # create salt and hash password
    salt = create_salt()
    hashed_pwd = hash_password(str(password + salt))

    # encode the token and format token
    token = jwt.encode({'user': username}, secret_key)
    token_decoded = 'Bearer ' + str(token.decode('UTF-8'))

    # create a new user and add to database
    new_user = UserModel(username, hashed_pwd, salt)
    new_user.save_to_db()

    # return the token
    return jsonify({'access_token': token_decoded}), 201


@users.route('/auth', methods=['POST'])
def auth():
    """
    input:
        - username
        - password
    output:
        - token
    """
    # take data from request
    data = request.get_json()

    # validate input
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    # information
    username = data['username']
    password = data['password']

    # query user
    user = db.session.query(UserModel).filter(UserModel.username == username).first()

    # if user is found
    if user:

        # password is correct
        if hash_password(password + user.salt) == user.password:

            # create token
            token = jwt.encode({'user': username}, secret_key)
            token_decoded = 'Bearer ' + str(token.decode('UTF-8'))

            # return decoded token
            return jsonify({'access_token': token_decoded}), 200

        # password is wrong
        else:
            return jsonify({'message': 'wrong password'}), 401

    # user not found
    else:
        return jsonify({'message': 'wrong username'}), 401
