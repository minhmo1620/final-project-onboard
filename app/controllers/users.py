import os
import random
import jwt
from marshmallow import ValidationError
from flask import Blueprint, request, jsonify

from app import db
from app.models.users import UserModel, UserSchema
from app.helpers import token_required, hash_password, validate_input

# create blueprint
users_blueprint = Blueprint('users', __name__)

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


# check the decorator
@users_blueprint.route('/check', methods=['POST'])
@token_required
def check(user_id):
    data = request.headers
    print(data["Authorization"].split())
    return jsonify({})


@users_blueprint.route('/users', methods=['POST'])
@validate_input(schema="user")
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
    token_decoded = 'Bearer ' + (token.decode('UTF-8'))

    # create a new user and add to database
    new_user = UserModel(username, hashed_pwd, salt)
    db.session.add(new_user)
    db.session.commit()

    # return the token
    return jsonify({'access_token': token_decoded}), 201


@users_blueprint.route('/auth', methods=['POST'])
@validate_input(schema="user")
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

    # information
    username = data['username']
    password = data['password']

    # query user
    user = db.session.query(UserModel).filter(UserModel.username == username).first()

    # if user is found
    if not user:
        return jsonify({'message': 'cannot find username'}), 404

    # password is wrong
    if hash_password(password + user.salt) != user.password:
        return jsonify({'message': 'wrong password'}), 401

    # create token
    token = jwt.encode({'user': username}, secret_key)
    token_decoded = 'Bearer ' + (token.decode('UTF-8'))

    # return decoded token
    return jsonify({'access_token': token_decoded}), 200
