from .default import Executor, ExecutorDefinition, registered_executor


class PayloadExecutorDefinition(ExecutorDefinition):
    def __init__(self, init):
        super(PayloadExecutorDefinition, self).__init__(init)
        self.payload = init.get('payload', '')


@registered_executor('payload')
class PayloadExecutor(Executor):
    Definition = PayloadExecutorDefinition

    def __init__(self, definition):
        super(PayloadExecutor, self).__init__(definition)