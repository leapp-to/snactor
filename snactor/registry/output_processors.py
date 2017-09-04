_REGISTERED_OUTPUT_PROCESSORS = {}


def get_output_processor(definition):
    if not isinstance(definition, dict):
        return None
    cls = _REGISTERED_OUTPUT_PROCESSORS[definition['type']]
    if cls:
        return cls(cls.Definition(definition))
    return None


def registered_output_processor(name):
    def func(cls):
        if name in _REGISTERED_OUTPUT_PROCESSORS:
            raise LookupError("Output processor '{}' has been already registered previously".format(name))
        cls.type = name
        _REGISTERED_OUTPUT_PROCESSORS[name] = cls
        return cls
    return func
