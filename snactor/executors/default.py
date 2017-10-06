import json
import logging
import os
import shlex
import tempfile
from contextlib import contextmanager
from six.moves import shlex_quote
from subprocess import Popen, PIPE

import jsonschema

from snactor.loader import get_loaded_path
from snactor.registry import get_environment_extension, must_get_schema
from snactor.utils.variables import resolve_variable_spec

_ACTOR_REMOTE_PATH = '/tmp/actors'


def validate_channel_data(channel, data):
    try:
        jsonschema.validate(data, must_get_schema(channel["name"], channel["version"]))
    except jsonschema.exceptions.ValidationError as error:
        msg = "Failed to validate channel '{}'. {}".format(channel["name"], channel["version"], str(error))
        raise jsonschema.exceptions.ValidationError(msg)


def filter_by_channel(channel_list, data):
    result = {}
    channels = {e['name']: e for e in channel_list}

    for k in data.keys():
        if k in channels.keys():
            validate_channel_data(channels[k]["type"], data[k])
            result[k] = data[k]
    return result


class Executor(object):
    def __init__(self, definition):
        self._environ = {}
        self.definition = definition
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
        if self.definition.output_processor:
            self.definition.output_processor.process(stdout, data)
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

    @staticmethod
    @contextmanager
    def _in_out_temp_files():
        input_file, output_file = tempfile.NamedTemporaryFile("r"), tempfile.NamedTemporaryFile("r")
        try:
            yield input_file, output_file
        finally:
            output_file.close()
            input_file.close()

    def execute_remote(self, data, address, user, sync_repo=True):
        actor_relative_path = os.path.relpath(self.definition.base_path, get_loaded_path())
        actor_remote_path = os.path.normpath(os.path.join(_ACTOR_REMOTE_PATH, actor_relative_path))
        input_data = filter_by_channel(self.definition.inputs, data)
        actor_input = self.handle_stdin(input_data)
        params = [str(resolve_variable_spec(data, a)) for a in self.definition.arguments]
        executable = self.definition.executable
        playbook = os.path.normpath(os.path.join(get_loaded_path(), '../playbooks/remote-execute-actor.yaml'))

        quoted_remote_command = ' '.join(shlex_quote(element) for element in [executable] + params)

        with self._in_out_temp_files() as (input_file, output_file):
            if actor_input:
                with open(input_file, 'r') as f:
                    f.write(actor_input)

            command_template = '''
                ansible-playbook
                        {playbook}
                        -i {host},
                        -u {user}
                        -e actor_repository="{actor_repo_path}"
                        -e sync_repo={sync_repo}
                        -e remote_host={host}
                        -e actor_output_file="{actor_output_file}"
                        -e actor_input_file="{actor_input_file}"
                        -e actor_command="'{actor_command}'"
                        -e actor_name="{actor_name}"
                        -e actor_cwd="{actor_cwd}"
                        -e actor_remote_repo_path="{remote_repo_path}"
            '''
            command = command_template.format(
                playbook=playbook,
                user=user,
                host=address,
                # Repo information
                actor_repo_path=get_loaded_path(),
                remote_repo_path=_ACTOR_REMOTE_PATH,
                sync_repo='True' if sync_repo else 'False',
                # actor configuration
                actor_name=self.definition.name,
                actor_command=quoted_remote_command,
                actor_cwd=actor_remote_path,
                actor_input_file=input_file.name,
                actor_output_file=output_file.name)

            ansible_process = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE)
            playbook_output = ansible_process.communicate()

            self.log.debug("PLAYBOOK STANDARD OUTPUT:\n------------------------\n%s\n----------------------",
                           playbook_output[0])
            self.log.debug("PLAYBOOK STANDARD ERROR:\n------------------------\n%s\n----------------------",
                           playbook_output[1])

            if ansible_process.returncode:
                return False

            with open(output_file.name, 'r') as f:
                actor_output = json.load(f)

            self.handle_stdout(actor_output['stdout'], data)
            self.handle_stderr(actor_output['stderr'], data)
            self.handle_return_code(actor_output['rc'], data)

            return actor_output['rc'] == 0

    def execute(self, data):
        if self.definition.remote:
            remote = self.definition.remote
            return self.execute_remote(data, resolve_variable_spec(data, remote.get('host', 'localhost')),
                                       resolve_variable_spec(data, remote.get('user', 'root')))
        input_data = filter_by_channel(self.definition.inputs, data)
        params = [str(resolve_variable_spec(data, a)) for a in self.definition.arguments]
        executable = self.definition.executable

        env = os.environ.copy()
        env.update(get_environment_extension())
        env.update(self._environ)
        p = Popen([executable] + params, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env,
                  cwd=self.definition.base_path)
        stdin = self.handle_stdin(input_data)
        out, err = p.communicate(stdin)
        self.handle_stderr(err, data)
        self.handle_stdout(out, data)
        p.wait()
        self.handle_return_code(p.returncode, data)
        return p.returncode == 0
