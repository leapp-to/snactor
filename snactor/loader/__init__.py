import logging
import os

import yaml

from snactor.definition import Definition
from snactor.loader.extends import ExtendsActor
from snactor.registry import register_actor, get_executor, get_actor


def _load(name, definition, tags, post_resolve):
    _log = logging.getLogger('snactor.loader')
    with open(definition) as f:
        _log.debug("Loading %s ...", definition)
        d = yaml.load(f)

        if tags:
            actor_tags = set(d.get('tags', ()))
            if not actor_tags or not actor_tags.intersection(tags):
                _log.debug("Skipping %s due to missing selected tags", definition)
                return

        if d.get('extends') and d.get('executor'):
            raise ValueError("Conflicting extends and executor specification found in {}".format(name))

        if not d.get('extends'):
            if not d.get('executor'):
                raise ValueError("Missing executor specification in {}".format(name))
            d['executor']['$location'] = os.path.abspath(definition)

        if d.get('extends') or not all(map(get_actor, d.get('executor', {}).get('actors', ()))):
            post_resolve[name] = {'definition': d, 'name': name, 'resolved': False}
            return

        create_actor(name, d)


def create_actor(name, definition):
    executor_name = definition.get('executor', {}).get('type')
    executor = get_executor(executor_name)
    if not executor:
        raise LookupError("Unknown executor {}".format(executor_name))

    definition.update({
        'executor': executor.Definition(definition.get('executor'))})
    register_actor(name, Definition(name, definition), executor)


def _apply_extension_resolve(data, base):
    definition = data['definition']
    definition['extended'] = base.definition
    register_actor(data['name'], definition, ExtendsActor)


def _try_resolve(current, to_resolve):
    if current['resolved']:
        return

    definition = current['definition']

    pending = definition.get('executor', {}).get('actors', ())
    if definition.get('extends'):
        pending = (definition['extends'].get('name'),)

    for name in pending:
        actor = get_actor(name)

        if not actor and name in to_resolve:
            if not to_resolve[name]['resolved']:
                _try_resolve(to_resolve[name], to_resolve)
            actor = get_actor(name)

        if not actor:
            raise LookupError("Failed to resolve dependencies for {}".format(current['name']))

    if definition.get('extends'):
        _apply_extension_resolve(current, get_actor(definition['extends'].get('name')))
    else:
        create_actor(current['name'], definition)

    current['resolved'] = True


def load(location, tags=()):
    post_resolve = {}
    tags = set(tags)
    for root, dirs, files in os.walk(location):
        if '_actor.yaml' in files:
            _load(os.path.basename(root), os.path.join(root, '_actor.yaml'), tags, post_resolve)
        else:
            for f in files:
                filename, ext = os.path.splitext(f)
                if not filename.startswith('.') and ext.lower() == '.yaml':
                    _load(filename, os.path.join(root, f), tags, post_resolve)

    for item in post_resolve.values():
        _try_resolve(item, post_resolve)
