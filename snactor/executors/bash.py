import snactor.output_processors  # noqa
from snactor.executors.script_file import ScriptFileExecutor
from snactor.executors.default import registered_executor
from snactor.registry import get_output_processor


class BashExecutorDefinition(ScriptFileExecutor.Definition):
    def __init__(self, init):
        super(BashExecutorDefinition, self).__init__(init)
        self.executable = "/bin/bash"
        self.output_processor = get_output_processor(init.get('output-processor', None))


@registered_executor('bash')
class BashExecutor(ScriptFileExecutor):
    Definition = BashExecutorDefinition

    def handle_stdout(self, stdout, data):
        self.log.debug("handle_stdout(%s)", stdout)
        if self.definition.executor.output_processor:
            self.definition.executor.output_processor.process(stdout, data)

    def __init__(self, definition):
        super(BashExecutor, self).__init__(definition)
