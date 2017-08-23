from snactor.executors.payload import PayloadExecutor, registered_executor


class PythonExecutorDefinition(PayloadExecutor.Definition):
    def __init__(self, init):
        super(PythonExecutorDefinition, self).__init__(init)
        self.executable = "/usr/bin/python"


@registered_executor('python')
class PythonExecutor(PayloadExecutor):
    Definition = PythonExecutorDefinition

    def __init__(self, definition):
        super(PythonExecutor, self).__init__(definition)
