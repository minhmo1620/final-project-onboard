from marshmallow import Schema, fields, validate, pre_load


class CategorySchema(Schema):
    name = fields.Str(validate=validate.Length(max=100, min=1),
                      required=True)
    description = fields.Str(validate=validate.Length(max=100, min=1),
                             required=True)

    @pre_load
    def strip_data(self, data, **kwargs):
        for key, value in data.items():
            if type(value) == str:
                data[key] = value.strip()
        return data
