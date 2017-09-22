import json
import logging
import os
import shlex
from subprocess import Popen, PIPE

import jsonschema

import snactor.output_processors  # noqa
from snactor.utils.variables import resolve_variable_spec
from snactor.definition import Definition
from snactor.registry import get_environment_extension, get_output_processor, must_get_schema, registered_executor


class ExecutorDefinition(object):
    def __init__(self, init):
        self.base_path = os.path.dirname(os.path.abspath(init['$location']))
        self.executable = init.get('executable', None)
        if self.executable and not os.path.isabs(self.executable):
            self.executable = os.path.abspath(os.path.join(self.base_path, self.executable))
        self.arguments = init.get('arguments', [])
        self.output_processor = get_output_processor(init.get('output-processor', None))
        self.script_file = init.get('script-file')
        if self.script_file:
            self.arguments.insert(0, self.script_file)


def validate_channel_data(channel, data):
    try:
        jsonschema.validate(data, must_get_schema(channel["type"]))
    except jsonschema.exceptions.ValidationError as error:
        msg = "Failed to validate channel '{}'. {}".format(channel["name"], str(error))
        raise jsonschema.exceptions.ValidationError(msg)


def filter_by_channel(channel_list, data):
    result = {}
    channels = {e['name']: e for e in channel_list}

    for k in data.keys():
        if k in channels.keys():
            validate_channel_data(channels[k], data[k])
            result[k] = data[k]
    return result


@registered_executor('default')
class Executor(object):
    Definition = ExecutorDefinition

    def __init__(self, definition):
        self._environ = {}
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
        if self.definition.executor.output_processor:
            self.definition.executor.output_processor.process(stdout, data)
        elif self.definition.outputs or stdout:
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

    def execute_remote(self, data, address, user):
        tpl = 'ansible -m synchronize -i {host}, all -u {user} -a "dest=/tmp/actors/ src={actor_dir} copy_links=yes'
        cmd = tpl.format(host=address, user=user, actor_dir=self.definition.executor.base_path)
        p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if p.returncode:
            self.log.error("Failed to synchronize actors\nError Code: %d\nStdOut:\n%s\nStdErr:\n%s\n", p.returncode,
                           stdout, stderr)
            return False

    def execute(self, data):
        input_data = filter_by_channel(self.definition.inputs, data)
        params = [str(resolve_variable_spec(data, a)) for a in self.definition.executor.arguments]
        executable = self.definition.executor.executable

        env = os.environ.copy()
        env.update(get_environment_extension())
        env.update(self._environ)
        p = Popen([executable] + params, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env,
                  cwd=self.definition.executor.base_path)
        stdin = self.handle_stdin(input_data)
        out, err = p.communicate(stdin)
        self.handle_stderr(err, data)
        self.handle_stdout(out, data)
        p.wait()
        self.handle_return_code(p.returncode, data)
        return p.returncode == 0
