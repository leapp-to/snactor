import os.path

import snactor.output_processors  # noqa
from snactor.registry.output_processors import get_output_processor
from snactor.registry.schemas import LATEST
from snactor.registry import must_get_actor


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
        self.base_path = os.path.dirname(os.path.abspath(init['$location']))
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

        self.remote = init.get('remote')
        execute = init.get('execute')
        if execute:
            self.executable = execute.get('executable', None)
            if self.executable and not os.path.isabs(self.executable):
                self.executable = os.path.abspath(os.path.join(self.base_path, self.executable))
            self.arguments = execute.get('arguments', [])
            self.output_processor = get_output_processor(execute.get('output-processor', None))
            self.script_file = execute.get('script-file')
            if self.script_file:
                self.arguments.insert(0, self.script_file)
        elif init.get('group'):
            self.actors = map(must_get_actor, init.get('group', ()))
