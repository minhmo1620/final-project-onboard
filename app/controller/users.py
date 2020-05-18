import random
import jwt
from flask import Blueprint, request, jsonify
from ..helpers import hash_password
from ..models.users import UserModel
from app import db
#cannot from app import app

users = Blueprint('users', __name__)
secret_key = "fwiefh3289fy3fh3efi23f392f"

#create random salt
def create_salt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []
    for i in range (16):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)


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
        return jsonify({'message': 'existed username'})

    salt = create_salt()

    hashed_pwd = hash_password(str(password+salt))

    token = jwt.encode({'user':username}, secret_key)

    token_decoded = token.decode('UTF-8')

    new_user = UserModel(username, hashed_pwd, salt, token_decoded)
    new_user.save_to_db()

    return jsonify({'message': 'created!'})


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
        return user.token
    else:
        return jsonify({'message':'wrong password or username'})


