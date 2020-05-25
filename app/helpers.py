import os
import hashlib
from functools import wraps

import jwt
from flask import jsonify, request
from marshmallow import ValidationError

from app.models.users import UserModel
from .db import db

# take secret key from .env
secret_key = str(os.getenv('SECRET_KEY'))


def hash_password(user_password):
    return hashlib.sha256(user_password.encode('utf-8')).hexdigest()


def token_required(f):
    """
    Decorator to validate the token and return user_id
    """

    @wraps(f)
    def wrapper(*arg, **kwargs):
        token = request.headers["Authorization"].split()
        if token[0] != "Bearer":
            return jsonify({"message": "Invalid token"}), 403
        try:
            data = jwt.decode(token[1], secret_key)
            username = data['user']
            user = db.session.query(UserModel).filter_by(username=username).first()
            if user is None:
                return jsonify({'message': 'Unauthenticated'}), 401

        except:
            return jsonify({'message': 'Token is invalid'}), 40
        return f(*arg, **kwargs, user_id=user.id)

    return wrapper


def validate_input(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # take the input
            data = request.get_json()

            # check the validity of the input
            try:
                schema().load(data)
            except ValidationError as err:
                return jsonify(err.messages), 400
            return f(*args, **kwargs, data=data)
        return wrapper
    return decorator

