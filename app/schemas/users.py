from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.Str(required=True,
                          validate=validate.Length(max=80, min=1))
    password = fields.Str(required=True,
                          validate=validate.Length(max=100, min=1))
    salt = fields.Str(required=True,
                      validate=validate.Length(max=20, min=1))
