from ..db import db
from marshmallow import Schema, fields


class CategoryModel(db.Model):
	__tablename__ = 'categories'

	# Columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(100))

	# relationship
	items = db.relationship('ItemModel')

	def __init__(self, category, description):
		self.name = category
		self.description = description

	# query by username
	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	# add object to database
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

# Marshmallow
class CategorySchema(Schema):
	name = fields.Str()
	description = fields.Str()

	class Meta:
		fields = ("name", "description")
