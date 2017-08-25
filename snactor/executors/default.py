import json
import logging
import os
from subprocess import Popen, PIPE

from snactor.utils.variables import resolve_variable_spec
from snactor.definition import Definition
from snactor.registry import registered_executor, get_environment_extension


class ExecutorDefinition(object):
    def __init__(self, init):
        self.base_path = os.path.dirname(os.path.abspath(init['$location']))
        self.executable = init.get('executable', None)
        if self.executable and not os.path.isabs(self.executable):
            self.executable = os.path.abspath(os.path.join(self.base_path, self.executable))
        self.arguments = init.get('arguments', [])


def filter_by_channel(channel_list, data):
    result = {}
    channels = set([e['name'] for e in channel_list])
    for k in data.keys():
        if k in channels:
            result[k] = data[k]
    return result


@registered_executor('default')
class Executor(object):
    Definition = ExecutorDefinition

    def __init__(self, definition):
        self.definition = definition or Definition(dict(executor=self.Definition({})))
        self.log = logging.getLogger(self.definition.name).getChild(self.__class__.__name__)

    def handle_stdin(self, input_data):
        self.log.debug("handle_stdin()")
        if self.definition.inputs:
            try:
                return json.dumps(input_data) + "\n"
            except (ValueError, OSError):
                self.log.warn("Writing input to stdin failed")
        return None

    def handle_stdout(self, stdout, data):
        self.log.debug("handle_stdout(%s)", stdout)
        if self.definition.outputs or stdout:
            try:
                output = filter_by_channel(self.definition.outputs, json.loads(stdout))
                data.update(output)
            except ValueError:
                self.log.warn("Failed to decode output: %s", stdout, exc_info=True)

    def handle_stderr(self, stderr, data):
        self.log.debug("handle_stderr(%s)", stderr)
        if stderr:
            self.log.info(stderr)

    def handle_return_code(self, return_code, data):
        self.log.debug("handle_return_code(%d)", return_code)

    def execute(self, data):
        input_data = filter_by_channel(self.definition.inputs, data)
        params = [resolve_variable_spec(data, a) for a in self.definition.executor.arguments]
        executable = self.definition.executor.executable

        env = os.environ.copy()
        env.update(get_environment_extension())
        p = Popen([executable] + params, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env)
        stdin = self.handle_stdin(input_data)
        out, err = p.communicate(stdin)
        self.handle_stderr(err, data)
        self.handle_stdout(out, data)
        p.wait()
        self.handle_return_code(p.returncode, data)
        return p.returncode == 0
