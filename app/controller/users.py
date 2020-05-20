import os
import random
import jwt
import requests
from flask import Blueprint, request, jsonify
from functools import wraps
from ..helpers import hash_password
from ..models.users import UserModel
from app import db

users = Blueprint('users', __name__)
secret_key = 'e9cac0f3f4Yd47a3be91d7b8f5'


#create random salt
def create_salt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range (16):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)


def token_required(f):
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


@users.route('/check', methods=['POST'])
@token_required
def check(token):
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

    data = request.get_json()

    username = data['username']
    password = data['password']

    if UserModel.find_by_username(username):
        return jsonify({'message': 'existed username'}), 400

    salt = create_salt()

    hashed_pwd = hash_password(str(password+salt))

    token = jwt.encode({'user': username}, secret_key)

    token_decoded = 'Bearer '+str(token.decode('UTF-8'))

    new_user = UserModel(username, hashed_pwd, salt)
    new_user.save_to_db()

    return jsonify({'access_token': token_decoded}), 201


@users.route('/auth', methods= ['POST'])
def auth():
    """
    input:
        - username
        - password
    output:
        - token
    """
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = db.session.query(UserModel).filter(UserModel.username == username).first()
    if user and hash_password(password + user.salt) == user.password:
        token = jwt.encode({'user': username}, secret_key)

        token_decoded = 'Bearer '+str(token.decode('UTF-8'))
        return jsonify({'access_token': token_decoded}), 200
    else:
        return jsonify({'message': 'wrong password or username'}), 401


