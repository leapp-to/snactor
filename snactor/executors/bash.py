from .payload import PayloadExecutor, registered_executor


class BashExecutorDefinition(PayloadExecutor.Definition):
    def __init__(self, init):
        super(BashExecutorDefinition, self).__init__(init)
        self.executable = "/bin/bash"


@registered_executor('bash')
class BashExecutor(PayloadExecutor):
    Definition = BashExecutorDefinition

    def __init__(self, definition):
        super(BashExecutor, self).__init__(definition)
