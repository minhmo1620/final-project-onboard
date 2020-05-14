from ..db import db


class CategoryModel(db.Model):
	__tablename__ = 'categories'

	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String(100))
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	users = db.relationship('UserModel')

	def __init__(self, category, creator_id):
		self.category = category
		self.creator_id = creator_id

	def json(self):
		return {'category': self.category}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(category=name).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
