from marshmallow import Schema, fields, validate, pre_load


class Base(Schema):
    @pre_load
    def strip_data(self, data, **kwargs):
        for key, value in data.items():
            if type(value) == str:
                data[key] = value.strip()
        return data