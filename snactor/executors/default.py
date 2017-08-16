from .registry import registered_executor


class ExecutorDefinition(object):

    def __init__(self, init):
        pass


@registered_executor('default')
class Executor(object):
    Definition = ExecutorDefinition

    def __init__(self, definition):
        self.definition = definition
