from ..db import db
from app import ma


class UserModel(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(100))

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()


class UserSchema(ma.Schema):
	class Meta:
		fields = ("id", "username")


user_schema = UserSchema()
users_schema = UserSchema(many=True)