from .payload import PayloadExecutor, PayloadExecutorDefinition, registered_executor


class BashExecutorDefinition(PayloadExecutorDefinition):
    def __init__(self, init):
        super(BashExecutorDefinition, self).__init__(init)


@registered_executor('bash')
class BashExecutor(PayloadExecutor):
    Definition = BashExecutorDefinition

    def __init__(self, definition):
        super(BashExecutor, self).__init__(definition)