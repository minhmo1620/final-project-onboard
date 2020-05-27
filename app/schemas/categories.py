from marshmallow import fields, validate
from .bases import Base


class CategorySchema(Base):
    name = fields.Str(validate=validate.Length(max=100, min=1),
                      required=True)
    description = fields.Str(validate=validate.Length(max=100, min=1),
                             required=True)
    id = fields.Int(required=False)
