import os

from snactor.loader import create_actor, load
from snactor.registry import get_registered_actors, must_get_actor
from snactor.utils import get_chan


class UnresolvedDependenciesError(Exception):
    """
    UnresolvedDependenciesError is thrown when the dependencies between actors can't be automatically resolved
    """
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
    """
    load_as_group creates a group actor with the given `name`, with actors loaded from `location` and is filtered
    by `tags`
    :param name: Name of the group actor to create
    :param location: Where to load the actors from
    :param tags: List of tags to filter by
    :return: A group actor ordered with resolved dependencies
    """
    load(location, tags)
    return _create_group_from_actors(name, get_registered_actors().values(), tags)


def create_group_from_names(name, names):
    """
    create_group_from_names creates a group actor named `name`, from a list of names specified in `names` (requires
    the actors to be loaded before)
    :param name: Name of the group actor to create
    :param names: List of actor names
    :return: A group actor ordered with resolved dependencies
    """
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
        'description': 'Auto generated group actor',
        'tags': tags or (),
    })
    return must_get_actor(name)
