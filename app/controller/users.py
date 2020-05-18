import random
from flask import Blueprint, request, jsonify
from ..helpers import hash_password
from ..models.users import UserModel

users = Blueprint('users', __name__)

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

    new_user = UserModel(username, hashed_pwd, salt)
    new_user.save_to_db()

    return jsonify({'message': 'created!'})



