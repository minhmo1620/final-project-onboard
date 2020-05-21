import hashlib

# from werkzeug.security import safe_str_cmp
# from .models.users import UserModel


def hash_password(users_password):
	"""
	hash user's password
	"""
	return hashlib.sha256(users_password.encode('utf-8')).hexdigest()


# def authenticate(username, password):
# 	user = UserModel.find_by_username(username)
# 	if user and safe_str_cmp(hash_password(user.password + user.salt), hash_password(password + user.salt)):
# 		return user
#
#
# def identity(payload):
# 	user_id = payload['identity']
# 	return UserModel.find_by_id(user_id)
