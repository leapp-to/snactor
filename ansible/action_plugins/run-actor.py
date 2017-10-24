from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os

from ansible.module_utils.six.moves import shlex_quote
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.action import ActionBase


def filter_by_channel(channel_list, data):
    result = {}
    channels = set([e['name'] for e in channel_list])

    for k in data.keys():
        if k in channels.keys():
            result[k] = data[k]
    return result


def resolve_variable_spec(data, spec):
    if data and spec.startswith('@') and spec.endswith('@'):
        for element in spec.strip('@').split('.'):
            data = data.get(element, None)
            if not data:
                break
        if data is None:
            raise ValueError("unresolved reference: {}".format(spec.strip("@")))
        return data
    return spec


# must be named ActionModule or it won't be seen by Ansible
class ActionModule(ActionBase):
    TRANSFERS_FILES = True

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()
        results = super(ActionModule, self).run(tmp, task_vars)

        actor_name = self._task.args['name']
        actor_repository = self._templar.template('{{ actor_repository }}')
        is_local = self._play_context.connection == 'local'
        task_vars['actor_remote_repo_path'] = actor_repository

        loader = DataLoader()
        loader.set_basedir(actor_repository)
        results.setdefault('ansible_facts', {}).setdefault('actor_inputs', self._task.args.setdefault('inputs', {}))
        results['ansible_facts']['actor_outputs'] = {}

        return self._perform(results, actor_name, loader, is_local)

    def _perform(self, results, actor_name, loader, is_local):
        actor = loader.load_from_file(os.path.join(actor_name, '_actor.yaml'), unsafe=True)

        if 'group' in actor:
            return self._perform_group(results, actor, loader, is_local)

        if not is_local:
            sync_result = self._repo_sync(actor_name)
            if sync_result['failed']:
                return sync_result

        results['ansible_facts']['actor_inputs'].update(results['ansible_facts']['actor_outputs'])

        inputs = filter_by_channel(actor.get('inputs', ()), results['ansible_facts']['actor_inputs'])

        executable = actor['execute']['executable']
        params = [str(resolve_variable_spec(inputs, a)) for a in actor['execute'].get('arguments', ())]
        if 'script-file' in actor['execute']:
            params.insert(0, actor['execute']['script-file'])
        command_result = self._low_level_execute_command(
                ' '.join(shlex_quote(element) for element in [executable] + params),
                in_data=json.dumps(inputs),
                chdir=self._templar.template("'{{actor_remote_repo_path}}/%s'" % actor_name))

        try:
            outputs = json.loads(command_result['stdout'])
            results['ansible_facts']['actor_outputs'].update(outputs)
        except ValueError:
            pass
        results.setdefault('actor_results', []).append(command_result)
        results['failed'] = command_result['rc'] != 0
        return results

    def _perform_group(self, results, group_data, loader, is_local):
        for actor in group_data['group']:
            results = self._perform(results, actor, loader, is_local)
            if results['failed']:
                # Stop on first error - As snactor does it
                break
        return results

    def _repo_sync(self, actor):
        args = {'src': self._templar.template("'{{actor_repository}}/'"),
                'dest': self._templar.template("'{{actor_remote_repo_path}}'"),
                'copy_links':'no',
                'delete': 'yes',
                'recursive':'yes',
                'links':'yes'}
        return self._execute_module(module_name='synchronize', module_args=args, task_vars=self._task.args)
