from ..db import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    items = db.relationship("ItemModel")

    def __init__(self, name, description):
        self.name = name
        self.description = description
