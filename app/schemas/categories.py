from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    name = fields.Str(validate=validate.Length(max=100, min=1),
                      required=True)
    description = fields.Str(validate=validate.Length(max=100, min=1),
                             required=True)
