import os

from snactor.loader import create_actor, load
from snactor.registry import get_registered_actors, must_get_actor
from snactor.utils import get_chan


class UnresolvedDependenciesError(Exception):
    pass


def _order_by_channels(channels, actors):
    result = []
    while actors:
        scheduled = []
        for idx, actor in enumerate(actors):
            for channel in actor[0].inputs:
                if channels[channel['name']]['producers']:
                    break
            else:
                # for channel in actor[0].inputs:
                #    channels[channel['name']]['consumers'].remove(actor[0].name)

                for channel in actor[0].outputs:
                    channels[channel['name']]['producers'].remove(actor[0].name)

                scheduled.append(idx)
                result.append(actor[0].name)

        if not scheduled:
            raise UnresolvedDependenciesError(
                "Could not solve dependency order for '{}'".format(', '.join([a[0].name for a in actors])))

        for idx in reversed(scheduled):
            actors.pop(idx)

    return result


def load_as_group(name, location, tags=()):
    load(location, tags)
    return _create_group_from_actors(name, get_registered_actors().values(), tags)


def create_group_from_names(name, names):
    return _create_group_from_actors(name, map(lambda x: get_registered_actors().get(x), names), None)


def _create_group_from_actors(name, actors, tags):
    channels = {}
    inputs, outputs = set(), set()

    skip_actors = set()
    for actor in actors:
        if actor[0].init.get('group'):
            skip_actors = skip_actors.union([a.definition.name for a in actor[0].actors])

    actor_list = []
    for actor in actors:
        if actor[0].name in skip_actors:
            continue
        actor_list.append(actor)

        for chan in actor[0].inputs:
            inputs.add(chan['name'])
            get_chan(channels, chan)['consumers'].append(actor[0].name)

        for chan in actor[0].outputs:
            outputs.add(chan['name'])
            get_chan(channels, chan)['producers'].append(actor[0].name)

    initial = inputs.difference(outputs)
    create_actor(name, {
        '$location': os.getcwd(),
        'inputs': [channels[chan]['data'] for chan in initial],
        'outputs': [channels[chan]['data'] for chan in outputs.difference(initial)],
        'group': _order_by_channels(channels, actor_list),
        'tags': tags or (),
    })
    return must_get_actor(name)
