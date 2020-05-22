import os
import hashlib
import jwt

from flask import jsonify, request
from functools import wraps
from marshmallow import ValidationError

from app.models.users import UserModel
from app.models.items import ItemSchema
from app.models.categories import CategorySchema

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


def validate_input(schema):
    def function(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            # take the input
            data = request.get_json()

            # check the validity of the input
            try:
                if schema == "item":
                    ItemSchema().load(data)
                elif schema == "category":
                    CategorySchema().load(data)
            except ValidationError as err:
                return jsonify(err.messages), 422
            return f(*args, **kwargs)
        return decorator
    return function
