_REGISTERED_EXECUTORS = {}


def get_executor(executor):
    return _REGISTERED_EXECUTORS.get(executor)


def registered_executor(name):
    def func(cls):
        if name in _REGISTERED_EXECUTORS:
            raise LookupError("Executor '{}' has been already registered previously".format(name))
        cls.type = name
        _REGISTERED_EXECUTORS[name] = cls
        return cls

    return func
