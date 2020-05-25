from marshmallow import Schema, fields
from ..db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    # Columns
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


# Marshmallow
class ItemSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    category_id = fields.Int()
    user_id = fields.Int()

    class Meta:
        fields = ("name", "description")
