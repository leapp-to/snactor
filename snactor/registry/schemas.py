_REGISTERED_SCHEMAS = {}


def must_get_schema(name):
    return _REGISTERED_SCHEMAS[name]


def get_schema(name):
    return _REGISTERED_SCHEMAS.get(name)


def register_schema(name, definition):
    if name in _REGISTERED_SCHEMAS and _REGISTERED_SCHEMAS[name] != definition:
        raise LookupError("Type schema '{}' has been already registered previously".format(name))
    _REGISTERED_SCHEMAS[name] = definition
