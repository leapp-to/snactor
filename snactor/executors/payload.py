import tempfile
import os.path

from .default import Executor, registered_executor


class PayloadExecutorDefinition(Executor.Definition):
    def __init__(self, init):
        super(PayloadExecutorDefinition, self).__init__(init)
        self.payload = init.get('payload', None) or ''
        self.arguments = init.get('arguments', [])
        self.script_file = init.get('script-file', None)
        if self.script_file:
            self.script_file = os.path.join(self.base_path, self.script_file)
        self.executable = init.get('executable', None)
        # TODO: warn about payload being unused when script-file defined


@registered_executor('payload')
class PayloadExecutor(Executor):
    Definition = PayloadExecutorDefinition

    def __init__(self, definition):
        super(PayloadExecutor, self).__init__(definition)

    def execute(self, data):
        if self.definition.executor.script_file:
            return self._execute_with_file(data)
        return self._execute_with_payload(data)

    def _execute_with_payload(self, data):
        with tempfile.NamedTemporaryFile() as f:
            self.definition.executor.arguments.insert(0, f.name)
            f.script_file = f.name
            f.write(self.definition.executor.payload)
            f.flush()
            return super(PayloadExecutor, self).execute(data)

    def _execute_with_file(self, data):
        self.definition.executor.arguments.insert(0, self.definition.executor.script_file)
        return super(PayloadExecutor, self).execute(data)
