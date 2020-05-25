from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)