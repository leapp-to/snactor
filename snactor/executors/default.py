import json
import logging
from subprocess import Popen, PIPE

from ..registry import registered_executor
from ..definition import Definition


class ExecutorDefinition(object):
    def __init__(self, init):
        self.executable = init.get('executable', None)
        self.arguments = init.get('arguments', [])


def resolve_variable_spec(data, spec):
    if data and spec.startswith('@') and spec.endswith('@'):
        for element in spec.strip('@').split('.'):
            if element in data:
                data = data.get(element, None)
            if not data:
                break
        if not data:
            raise ValueError("unresolved reference")
        return data
    return spec


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
        try:
            output = filter_by_channel(self.definition.output, json.loads(stdout))
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
        p = Popen([executable] + params, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdin = self.handle_stdin(input_data)
        out, err = p.communicate(stdin)
        self.handle_stderr(err, data)
        self.handle_stdout(out, data)
        p.wait()
        self.handle_return_code(p.returncode, data)
        return p.returncode == 0
