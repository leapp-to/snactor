from marshmallow.schema import Schema, fields


class OSVersion(Schema):
    name = fields.String()
    version = fields.String()
