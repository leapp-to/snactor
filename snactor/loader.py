import os
import yaml
from .executors.default import ExecutorDefinition
from .registry import registered_actor, get_executor, get_actor
from .definition import Definition
from .utils.variables import resolve_variable_spec


def _load(name, definition, tags, post_resolve):
    with open(definition) as f:
        print("Loading", definition, "...")
        d = yaml.load(f)

        if tags:
            actor_tags = set(d.get('tags', ()))
            if not actor_tags or not actor_tags.intersection(tags):
                print("Skipping", definition, "due to missing selected tags")
                return

        if d.get('extends') and d.get('executor'):
            raise ValueError("Conflicting extends and executor specification found in {}".format(name))
        if d.get('extends'):
            post_resolve[name] = {'definition': d, 'name': name, 'resolved': False}
        else:
            executor_name = d.get('executor', {}).get('type')
            executor = get_executor(executor_name)
            if not executor:
                raise LookupError("Unknown executor {}".format(executor_name))

            d['executor']['$location'] = os.path.abspath(definition)
            d.update({
                'executor': executor.Definition(d.get('executor'))})
            create_actor(name, d, executor)


def create_actor(name, definition, executor):
    @registered_actor(name)
    class Actor(executor):
        Executor = executor

        def __init__(self):
            super(Actor, self).__init__(Definition(name, definition))


class ExtendsActorDefinition(ExecutorDefinition):
    def __init__(self, init):
        self.extended = init['extended']
        self.required_inputs = init.get('inputs', ())
        self.inputs = init.get('extends', {}).get('inputs', ())
        self.output = init.get('extends', {}).get('outputs', ())
        self.restricted_inputs = [i['name'] for i in self.extended.inputs]


def _create_extends_actor(name, definition, executor):
    @registered_actor(name)
    class ExtendsActor(executor):
        Definition = ExtendsActorDefinition

        def execute(self, data):
            extends = ExtendsActorDefinition(definition)
            restricted = {n['name']: data[n['name']] for n in extends.required_inputs}
            restricted.update({i['name']: resolve_variable_spec(restricted, i['source']) for i in extends.inputs if 'source' in i})
            restricted.update({i['name']: i['value'] for i in extends.inputs if 'value' in i})

            ret = super(ExtendsActor, self).execute(restricted)
            if ret:
                for output in extends.output:
                    data[output['name']] = resolve_variable_spec(restricted, output['source'])

            return ret


def _apply_resolve(extends, base):
    definition = extends['definition']
    definition['extended'] = base().definition
    _create_extends_actor(extends['name'], definition, base)


def _try_resolve(i, l):
    if not i['resolved']:
        name = i['definition']['extends'].get('name')
        actor = get_actor(name)

        if not actor and name in l:
            if not l[name]['resolved']:
                _try_resolve(l[name], l)
            actor = get_actor(name)

        if not actor:
            raise LookupError("Failed to resolve dependencies for {}".format(i['name']))

        _apply_resolve(i, actor)
        i['resolved'] = True


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

    for i in post_resolve.values():
        _try_resolve(i, post_resolve)
