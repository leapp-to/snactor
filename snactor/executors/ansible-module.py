from snactor.executors.default import Executor, registered_executor


class AnsibleModuleExecutorDefinition(Executor.Definition):
    def __init__(self, init):
        super(AnsibleModuleExecutorDefinition, self).__init__(init)
        self.module = init.get('module', None)
        self.host = init.get('host', None)
        self.user = init.get('user', 'root')
        self.target = init.get('output', '__drop')


@registered_executor('ansible-module')
class AnsibleModuleExecutor(Executor):
    Definition = AnsibleModuleExecutorDefinition

    def handle_stdout(self, stdout, data):
        if stdout.strip():
            _, stdout = stdout.split('|')
            result, stdout = stdout.split('=>', 1)
            self.result = result.strip().upper() == 'SUCCESS'
            stdout = '{"%s": %s}' % (self.definition.executor.target, stdout)
        return super(AnsibleModuleExecutor, self).handle_stdout(stdout, data)

    def __init__(self, definition):
        super(AnsibleModuleExecutor, self).__init__(definition)
        self.result = False

    def execute(self, data):
        self.result = False
        self.definition.executor.executable = 'ansible'

        self.definition.executor.arguments = [
            '-C', '-cssh',
            '-m', self.definition.executor.module or 'setup',
            '-u', self.definition.executor.user]
        if self.definition.executor.host and self.definition.executor.host != 'localhost':
            self.definition.executor.arguments.extend([
                '-i', self.definition.executor.host + ',', 'all'
            ])
        else:
            self.definition.executor.arguments.append('localhost')
        self.log.debug("Executing: %s %s",
                       self.definition.executor.executable,
                       ' '.join(self.definition.executor.arguments))
        super(AnsibleModuleExecutor, self).execute(data)
        return self.result
