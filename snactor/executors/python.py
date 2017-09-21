from snactor.executors.script_file import ScriptFileExecutor
from snactor.executors.default import registered_executor


class PythonExecutorDefinition(ScriptFileExecutor.Definition):
    def __init__(self, init):
        super(PythonExecutorDefinition, self).__init__(init)
        self.executable = "/usr/bin/python"


@registered_executor('python')
class PythonExecutor(ScriptFileExecutor):
    Definition = PythonExecutorDefinition

    def __init__(self, definition):
        super(PythonExecutor, self).__init__(definition)
