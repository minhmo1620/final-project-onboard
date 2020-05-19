from ..db import db
# from .. import ma
from marshmallow import Schema

class ItemModel(db.Model):
	__tablename__ = "items"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(200))
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __init__(self, name, description, category_id, user_id):
		self.name = name
		self.description = description
		self.category_id = category_id
		self.user_id = user_id

	def json(self):
		return {'name': self.name, 'description': self.description}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first() 

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()


class ItemSchema(Schema):
	class Meta:
		fields = ("name", "description")


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
