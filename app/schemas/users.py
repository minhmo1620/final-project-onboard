from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.Str(required=True,
                          validate=validate.Length(max=80))
    password = fields.Str(required=True,
                          validate=validate.Length(max=100))
    salt = fields.Str(required=True,
                      validate=validate.Length(max=20))
