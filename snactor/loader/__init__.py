import imp
import logging
import os
import sys

import yaml

from snactor.definition import Definition
from snactor.registry import register_actor, get_actor, get_registered_actors, get_schema

_LOADED_ACTOR_PATH = None


def get_loaded_path():
    return _LOADED_ACTOR_PATH


def _load(name, definition, tags, post_resolve):
    _log = logging.getLogger('snactor.loader')
    with open(definition) as f:
        _log.debug("Loading %s ...", definition)
        d = yaml.load(f)
        d['$location'] = os.path.abspath(definition)

        if tags:
            actor_tags = set(d.get('tags', ()))
            if not actor_tags.intersection(tags):
                _log.debug("Skipping %s due to missing selected tags", definition)
                return

        if not d.get('execute') and not d.get('group'):
            raise ValueError("Missing execute or group specification in {}".format(name))

        if not all(map(get_actor, d.get('group', ()))):
            d['$location'] = os.path.abspath(definition)
            post_resolve[name] = {'definition': d, 'name': name, 'resolved': False}
            return

        create_actor(name, d)


def create_actor(name, definition):
    from snactor.executors.default import Executor
    from snactor.executors.group import GroupExecutor

    executor = Executor
    if definition.get('group', None):
        executor = GroupExecutor
    register_actor(name, Definition(name, definition), executor)


def _try_resolve(current, to_resolve):
    if current['resolved']:
        return

    definition = current['definition']

    pending = definition.get('group', ())
    for name in pending:
        actor = get_actor(name)

        if not actor and name in to_resolve:
            if not to_resolve[name]['resolved']:
                _try_resolve(to_resolve[name], to_resolve)
            actor = get_actor(name)

        if not actor:
            raise LookupError("Failed to resolve dependency '{}' for {}".format(name, current['name']))

    create_actor(current['name'], definition)

    current['resolved'] = True


def load(location, tags=()):
    global _LOADED_ACTOR_PATH
    _LOADED_ACTOR_PATH = os.path.abspath(location)

    post_resolve = {}
    tags = set(tags)
    for root, dirs, files in os.walk(location):
        if '_actor.yaml' in files:
            if "schema" in dirs:
                load_schemas(os.path.join(root, "schema"))

            _load(os.path.basename(root), os.path.join(root, '_actor.yaml'), tags, post_resolve)
        else:
            for f in files:
                filename, ext = os.path.splitext(f)
                if not filename.startswith('.') and ext.lower() == '.yaml':
                    _load(filename, os.path.join(root, f), tags, post_resolve)

    for item in post_resolve.values():
        _try_resolve(item, post_resolve)


def _validate_type(actor_name, direction, type_definition):
    _log = logging.getLogger('snactor.loader')
    if not get_schema(type_definition["name"], type_definition["version"]):
        _log.warning("Could not resolve schema for type %s@%s on %s in actor %s",
                     type_definition["name"],
                     type_definition["version"],
                     direction,
                     actor_name)
        return False, (type_definition["name"], direction, actor_name)
    return True, None


class ActorTypeValidationError(LookupError):
    def __init__(self, message, data):
        super(ActorTypeValidationError, self).__init__(message)
        self.data = data


def validate_actor_types():
    result = []
    for name, (definition, _) in get_registered_actors().items():
        result.extend((_validate_type(name, 'inputs', current['type']) for current in definition.inputs))
        result.extend((_validate_type(name, 'outputs', current['type']) for current in definition.outputs))
    if not all((item[0] for item in result)):
        raise ActorTypeValidationError("Failed to lookup schema definitions", (x[1] for x in result if not x[0]))


def load_schemas(location):
    _log = logging.getLogger('snactor.loader')
    sys.path.append(location)

    for root, dirs, files in os.walk(location):
        for schema_file in files:
            module_name, ext = os.path.splitext(schema_file)
            if not module_name.startswith('.') and ext.lower() == '.py':
                _log.debug("Loading schema(s) from  %s", os.path.join(root, schema_file))
                f, path, description = imp.find_module(module_name, [root])
                # Load schema module
                imp.load_module(module_name, f, path, description)

    sys.path.pop()
