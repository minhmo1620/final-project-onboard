import os
import hashlib
import jwt
from flask import jsonify, request
from functools import wraps
from app.models.users import UserModel


# take secret key from .env
secret_key = str(os.getenv('SECRET_KEY'))


def hash_password(users_password):
    """
    hash user's password
    """
    return hashlib.sha256(users_password.encode('utf-8')).hexdigest()


def token_required(f):
    """
    Decorator to validate the token and return user_id
    """

    @wraps(f)
    def decorator(*arg, **kwargs):
        token = request.headers["Authorization"].split()
        if token[0] != "Bearer":
            return jsonify({"message": "Invalid token"}), 401
        try:
            data = jwt.decode(token[1], secret_key)
            username = data['user']
            user = UserModel.find_by_username(username)
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*arg, **kwargs, user_id=user.id)

    return decorator
