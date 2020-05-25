from marshmallow import Schema, fields, validate


class CreateItem(Schema):
    name = fields.Str(required=True,
                      validate=validate.Length(max=100, min=1))
    description = fields.Str(required=True,
                             validate=validate.Length(max=200, min=1))


class ItemSchema(Schema):
    name = fields.Str(required=False,
                      validate=validate.Length(max=100, min=1))
    description = fields.Str(required=True,
                             validate=validate.Length(max=200, min=1))