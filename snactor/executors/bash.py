from .payload import PayloadExecutor, registered_executor
from ..registry import get_output_processor


class BashExecutorDefinition(PayloadExecutor.Definition):
    def __init__(self, init):
        super(BashExecutorDefinition, self).__init__(init)
        self.executable = "/bin/bash"
        self.output = get_output_processor(init.get('output', None))


@registered_executor('bash')
class BashExecutor(PayloadExecutor):
    Definition = BashExecutorDefinition

    def __init__(self, definition):
        super(BashExecutor, self).__init__(definition)
