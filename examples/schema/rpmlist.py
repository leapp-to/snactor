from marshmallow.schema import Schema, fields


class RPMPackage(Schema):
    name = fields.String()
    version = fields.String()


class RPMPackages(Schema):
    packages = fields.List(RPMPackage)
