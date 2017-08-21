import os
import yaml
from .registry import registered_actor, get_executor
from .definition import Definition


def _load(name, definition, post_resolve):
    with open(definition) as f:
        print("Loading", definition, "...")
        d = yaml.load(f)
        if d.get('extends'):
            post_resolve.append(d)
        else:
            executor_name = d.get('executor', {}).get('type')
            executor = get_executor(executor_name)
            if not executor:
                raise ValueError("Unknown executor {}".format(executor_name))

            d.update({
                'executor': executor.Definition(d.get('executor'))})

            @registered_actor(name)
            class Actor(executor):
                def __init__(self):
                    super(Actor, self).__init__(Definition(name, d))


def load(location):
    post_resolve = []
    for root, dirs, files in os.walk(location):
        if '_actor.yaml' in files:
            _load(os.path.basename(root), os.path.join(root, '_actor.yaml'), post_resolve)
        else:
            for f in files:
                _load(os.path.splitext(f)[0], os.path.join(root, f), post_resolve)
