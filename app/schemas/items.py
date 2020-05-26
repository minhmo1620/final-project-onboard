from marshmallow import Schema, fields, validate, pre_load


class CreateItem(Schema):
    name = fields.Str(required=True,
                      validate=validate.Length(max=100, min=1))
    description = fields.Str(required=True,
                             validate=validate.Length(max=200, min=1))

    @pre_load
    def strip_data(self, data, **kwargs):
        data["name"] = data["name"].strip()
        data["description"] = data["description"].strip()


class ItemSchema(Schema):
    name = fields.Str(required=False,
                      validate=validate.Length(max=100, min=1))
    description = fields.Str(required=True,
                             validate=validate.Length(max=200, min=1))

    @pre_load
    def strip_data(self, data, **kwargs):
        data["name"] = data["name"].strip()
        data["description"] = data["description"].strip()
