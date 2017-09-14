import json
from six.moves import shlex_quote

from snactor.executors.ansible_module import AnsibleModuleExecutor, registered_executor, resolve_variable_spec


class AnsibleScriptModuleExecutorDefinition(AnsibleModuleExecutor.Definition):
    def __init__(self, init):
        super(AnsibleScriptModuleExecutorDefinition, self).__init__(init)
        self.module = {'name': 'script', 'arguments': [init['script-file']] + init.get('arguments', [])}


@registered_executor('ansible-script-module')
class AnsibleScriptModuleExecutor(AnsibleModuleExecutor):
    Definition = AnsibleScriptModuleExecutorDefinition

    def handle_stdout(self, stdout, data):
        if stdout.strip():
            source, stdout = stdout.split('|', 1)
            result, stdout = stdout.split('=>', 1)
            self.result = result.strip().upper() == 'SUCCESS'
            if self.result:
                try:
                    stdout = json.loads(stdout)["stdout"]
                except (ValueError, KeyError) as e:
                    stdout = str(e)
            else:
                try:
                    self.log.info("Module execution failed:\n%s", json.loads(stdout)["stderr"])
                except (ValueError, KeyError):
                    pass
        # Yes we do want the base of AnsibleModuleExecutor to bypass that implementation
        return super(AnsibleModuleExecutor, self).handle_stdout(stdout, data)

    def __init__(self, definition):
        super(AnsibleScriptModuleExecutor, self).__init__(definition)

    def execute(self, data):
        translated = (resolve_variable_spec(data, item) for item in self.definition.executor.module['arguments'])
        translated = [shlex_quote(json.dumps(item)) if isinstance(item, dict) else str(item)for item in translated]
        user = resolve_variable_spec(data, self.definition.executor.user)
        prefix = ['sudo'] if user != 'root' else []
        self.definition.executor.module['arguments'] = [' '.join(prefix + translated)]
        return super(AnsibleScriptModuleExecutor, self).execute(data)
