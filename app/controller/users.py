import random
from flask import Blueprint
from ..helpers import hash_password

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
    input: username, password
    output:
        - raise error if username is existed
        - if username is not existed
            - create new salt
            - hash password
            --> create new user (username, hashed password, salt)
    """
    pass