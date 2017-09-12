from snactor.executors.default import Executor, registered_executor
from snactor.utils.variables import resolve_variable_spec, resolve_variable_spec_items


class AnsibleModuleExecutorDefinition(Executor.Definition):
    def __init__(self, init):
        super(AnsibleModuleExecutorDefinition, self).__init__(init)
        self.module = init.get('module', {})
        self.host = init.get('host', None)
        self.user = init.get('user', 'root')
        self.target = init.get('output', '__drop')


@registered_executor('ansible-module')
class AnsibleModuleExecutor(Executor):
    Definition = AnsibleModuleExecutorDefinition

    def handle_stdout(self, stdout, data):
        if stdout.strip():
            _, stdout = stdout.split('|', 1)
            result, stdout = stdout.split('=>', 1)
            self.result = result.strip().upper() == 'SUCCESS'
            stdout = '{"%s": %s}' % (self.definition.executor.target, stdout)
        else:
            stdout = "{}"
        return super(AnsibleModuleExecutor, self).handle_stdout(stdout, data)

    def __init__(self, definition):
        super(AnsibleModuleExecutor, self).__init__(definition)
        self.result = False

    def execute(self, data):
        self.result = False
        self.definition.executor.executable = 'ansible'
        host = resolve_variable_spec(data, self.definition.executor.host) or 'localhost'
        user = resolve_variable_spec(data, self.definition.executor.user)

        self._environ["ANSIBLE_HOST_KEY_CHECKING"] = "False"
        self.definition.executor.arguments = [
            '-m', self.definition.executor.module['name'] or 'setup',
            '-u', user, '-i', host + ',', 'all',
        ]
        self.definition.executor.arguments.append('-clocal' if host in ('localhost', '127.0.0.1') else '-cssh')

        args = self.definition.executor.module.get('arguments', ())
        if args:
            self.definition.executor.arguments.append('--args')
            if not isinstance(args, (tuple, list)):
                args = (args,)
            self.definition.executor.arguments.extend(resolve_variable_spec_items(data, args))

        self.log.debug('Executing: %s %s',
                       self.definition.executor.executable,
                       ' '.join(self.definition.executor.arguments))
        super(AnsibleModuleExecutor, self).execute(data)
        return self.result
