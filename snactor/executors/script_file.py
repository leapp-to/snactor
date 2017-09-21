import os.path

from snactor.executors.default import Executor


class ScriptFileExecutorDefinition(Executor.Definition):
    def __init__(self, init):
        super(ScriptFileExecutorDefinition, self).__init__(init)
        self.arguments = init.get('arguments', [])
        self.script_file = init['script-file']
        self.script_file = os.path.join(self.base_path, self.script_file)
        self.executable = init.get('executable', None)


class ScriptFileExecutor(Executor):
    Definition = ScriptFileExecutorDefinition

    def __init__(self, definition):
        super(ScriptFileExecutor, self).__init__(definition)

    def execute(self, data):
        self.definition.executor.arguments.insert(0, self.definition.executor.script_file)
        return super(ScriptFileExecutor, self).execute(data)
