_REGISTERED_ACTORS = {}
_REGISTERED_EXECUTORS = {}
_REGISTERED_OUTPUT_PROCESSORS = {}
_REGISTERED_ENVIRON_VARS = {}


def get_executor(executor):
    return _REGISTERED_EXECUTORS.get(executor)


def get_actor(actor):
    return _REGISTERED_ACTORS.get(actor)


def must_get_actor(actor):
    return _REGISTERED_ACTORS[actor]


def get_output_processor(definition):
    if not isinstance(definition, dict):
        return None
    cls = _REGISTERED_OUTPUT_PROCESSORS[definition['type']]
    if cls:
        return cls(cls.Definition(definition))
    return None


def get_environment_extension():
    return _REGISTERED_ENVIRON_VARS


def register_environment_variable(name, value):
    if name in _REGISTERED_ENVIRON_VARS:
        raise LookupError(
            "Environment variable '{}' has been already registered previously with value {}".format(
                name, _REGISTERED_ENVIRON_VARS[name]))
    _REGISTERED_ENVIRON_VARS[name] = value


def registered_output_processor(name):
    def func(cls):
        if name in _REGISTERED_OUTPUT_PROCESSORS:
            raise LookupError("Output processor '{}' has been already registered previously".format(name))
        cls.type = name
        _REGISTERED_OUTPUT_PROCESSORS[name] = cls
        return cls
    return func


def registered_executor(name):
    def func(cls):
        if name in _REGISTERED_EXECUTORS:
            raise LookupError("Executor '{}' has been already registered previously".format(name))
        cls.type = name
        _REGISTERED_EXECUTORS[name] = cls
        return cls

    return func


def registered_actor(name):
    def func(cls):
        if name in _REGISTERED_ACTORS:
            raise LookupError("Actor '{}' has been already registered previously".format(name))
        cls.type = name
        _REGISTERED_ACTORS[name] = cls
        return cls

    return func
