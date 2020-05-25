from marshmallow import Schema, fields
from ..db import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))

    # relationship
    items = db.relationship('ItemModel')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    # query by username
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


# Marshmallow
class CategorySchema(Schema):
    name = fields.Str()
    description = fields.Str()
