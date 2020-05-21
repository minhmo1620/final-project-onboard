import hashlib


def hash_password(users_password):
    """
    hash user's password
    """
    return hashlib.sha256(users_password.encode('utf-8')).hexdigest()


