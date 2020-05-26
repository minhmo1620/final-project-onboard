from marshmallow import fields, validate
from .bases import Base


class UpdateItem(Base):
    description = fields.Str(required=True,
                             validate=validate.Length(max=200, min=1))


class ItemSchema(Base):
    name = fields.Str(required=True,
                      validate=validate.Length(max=100, min=1))
    description = fields.Str(required=True,
                             validate=validate.Length(max=200, min=1))
