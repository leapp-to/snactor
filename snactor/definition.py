from snactor.registry.schemas import LATEST


class Definition(object):
    def __resolve_channel_type(self, channels):
        """
            Resolve type of input / output channel. The version field is optional and if
            not set, a LATEST is used as a string identifier.

            type:
              name: Name
              version: Version
        """
        for channel in channels:
            channel["type"].setdefault("version", LATEST)

    def __init__(self, name, init=None):
        init = init or {}
        self.name = name
        self.tags = set(init.get('tags', ()))
        self.inputs = init.get('inputs', ())
        self.__resolve_channel_type(self.inputs)

        self.outputs = init.get('outputs', ())
        if not isinstance(self.outputs, (list, tuple)):
            self.outputs = (self.outputs,)
        self.__resolve_channel_type(self.outputs)

        self.description = init.get('description', 'No description has been provided for this actor')
        self.executor = init.get('executor', None)
