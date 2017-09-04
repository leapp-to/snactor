_REGISTERED_ENVIRON_VARS = {}


def get_environment_extension():
    return _REGISTERED_ENVIRON_VARS


def register_environment_variable(name, value):
    if name in _REGISTERED_ENVIRON_VARS:
        raise LookupError(
            "Environment variable '{}' has been already registered previously with value {}".format(
                name, _REGISTERED_ENVIRON_VARS[name]))
    _REGISTERED_ENVIRON_VARS[name] = value
