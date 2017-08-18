from .default import Executor, ExecutorDefinition, registered_executor


class ReturnCodeExecutorDefinition(ExecutorDefinition):
    def __init__(self, init):
        super(ReturnCodeExecutorDefinition, self).__init__(init)


@registered_executor('return-code')
class ReturnCodeExecutor(Executor):
    Definition = ReturnCodeExecutorDefinition

    def __init__(self, definition):
        super(ReturnCodeExecutor, self).__init__(definition)
