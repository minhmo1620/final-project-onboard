from app import db
from marshmallow import Schema, fields


class UserModel(db.Model):
	__tablename__ = "users"

	# Columns
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(100))
	salt = db.Column(db.String(100))

	# relationship
	items = db.relationship('ItemModel')

	# attributes
	def __init__(self, username, password, salt):
		self.username = username
		self.password = password
		self.salt = salt

	# add object to database
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	# query by username
	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()


# Marshmallow
class UserSchema(Schema):
	username = fields.Str()
	password = fields.Str()
	salt = fields.Str()
