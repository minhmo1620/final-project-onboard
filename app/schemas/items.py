from marshmallow import Schema, fields, validate, pre_load


class UpdateItem(Schema):
    description = fields.Str(required=True,
                             validate=validate.Length(max=200, min=1))

    @pre_load
    def strip_data(self, data, **kwargs):
        for key, value in data.items():
            if type(value) == str:
                data[key] = value.strip()
        return data


class ItemSchema(Schema):
    name = fields.Str(required=False,
                      validate=validate.Length(max=100, min=1))
    description = fields.Str(required=True,
                             validate=validate.Length(max=200, min=1))

    @pre_load
    def strip_data(self, data, **kwargs):
        for key, value in data.items():
            if type(value) == str:
                data[key] = value.strip()
        return data
