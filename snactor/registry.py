_REGISTERED_ACTORS = {}
_REGISTERED_EXECUTORS = {}
_REGISTERED_OUTPUT_PROCESSORS = {}


def get_executor(executor):
    return _REGISTERED_EXECUTORS.get(executor)


def get_actor(actor):
    return _REGISTERED_ACTORS.get(actor)


def get_output_processor(definition):
    if not isinstance(definition, dict):
        return None
    cls = _REGISTERED_ACTORS.get(definition.get('type'), None)
    if cls:
        return cls(cls.Definition(definition))
    return None


def registered_output_processor(name):
    def func(cls):
        if name in _REGISTERED_OUTPUT_PROCESSORS:
            raise ValueError("Output processor '{}' has been already registered previously".format(name))
        cls.type = name
        _REGISTERED_OUTPUT_PROCESSORS[name] = cls
        return cls
    return func


def registered_executor(name):
    def func(cls):
        if name in _REGISTERED_EXECUTORS:
            raise ValueError("Executor '{}' has been already registered previously".format(name))
        cls.type = name
        _REGISTERED_EXECUTORS[name] = cls
        return cls
    return func


def registered_actor(name):
    def func(cls):
        if name in _REGISTERED_ACTORS:
            raise ValueError("Actor '{}' has been already registered previously".format(name))
        cls.type = name
        _REGISTERED_ACTORS[name] = cls
        return cls
    return func

