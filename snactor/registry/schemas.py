_REGISTERED_SCHEMAS = {}

LATEST = "latest"


def registered_schema(versions):
    def func(schema):
        # Shout that there are no versions?
        if not versions:
            raise ValueError("Cannot register schema {}, no version was specified".format(schema.__name__))

        for version in versions:
            # _log.debug("Loading schema %s@%s from %s...",
            #           schema.__name__,
            #           version, os.path.join(root, schema_file))
            register_schema(schema.__name__, version, schema.get_schema(version))

        # register latest version of schema as "latest"
        register_schema(schema.__name__, LATEST, schema.get_schema(versions[-1]))

        return schema

    return func


def must_get_schema(name, version):
    return _REGISTERED_SCHEMAS["{}-{}".format(name, version)]


def get_schema(name, version):
    return _REGISTERED_SCHEMAS.get("{}-{}".format(name, version))


def register_schema(name, version, definition):
    existing = get_schema(name, version)

    if existing is not None and existing != definition:
        raise LookupError("Type schema '{}' has been already registered previously".format(name))

    _REGISTERED_SCHEMAS["{}-{}".format(name, version)] = definition
