from marshmallow import Schema, fields, validate, pre_load


class UserSchema(Schema):
    username = fields.Str(required=True,
                          validate=validate.Length(max=80, min=1))
    password = fields.Str(required=True,
                          validate=validate.Length(max=100, min=1))

    @pre_load
    def strip_data(self, data, **kwargs):
        data["username"] = data["name"].strip()
