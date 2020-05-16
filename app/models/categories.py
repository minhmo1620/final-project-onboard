from ..db import db
# from .. import ma
from marshmallow import Schema

class CategoryModel(db.Model):
	__tablename__ = 'categories'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(100))

	items = db.relationship('ItemModel')

	def __init__(self, category, description):
		self.name = category
		self.description = description

	def json(self):
		return {'category': self.category}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(category=name).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()


class CategorySchema(Schema):
	class Meta:
		fields = ("name", "description")


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)