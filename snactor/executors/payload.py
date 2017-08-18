import tempfile

from .default import Executor, registered_executor


class PayloadExecutorDefinition(Executor.Definition):
    def __init__(self, init):
        super(PayloadExecutorDefinition, self).__init__(init)
        self.payload = init.get('payload', None) or ''
        self.arguments = init.get('arguments', [])
        self.executable = init.get('executable', None)


@registered_executor('payload')
class PayloadExecutor(Executor):
    Definition = PayloadExecutorDefinition

    def __init__(self, definition):
        super(PayloadExecutor, self).__init__(definition)

    def execute(self, data):
        with tempfile.NamedTemporaryFile() as f:
            self.definition.executor.arguments.insert(0, f.name)
            f.write(self.definition.executor.payload)
            f.flush()
            return super(PayloadExecutor, self).execute(data)
