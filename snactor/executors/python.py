from .payload import PayloadExecutor, PayloadExecutorDefinition, registered_executor


class PythonExecutorDefinition(PayloadExecutorDefinition):
    def __init__(self, init):
        super(PythonExecutorDefinition, self).__init__(init)


@registered_executor('python')
class PythonExecutor(PayloadExecutor):

    Definition = PayloadExecutorDefinition

    def __init__(self, definition):
        super(PythonExecutor, self).__init__(definition)
        self.execute = "/usr/bin/python"
        self.arguments = ["-"]

