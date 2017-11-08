from snactor.registry import get_registered_actors
from snactor.utils import get_chan

import pydot


def convert_to_graph(actors=None):
    g = pydot.Graph()

    channels = {}
    names = set()
    if actors:
        iterable = ((actor.definition, None) for actor in actors)
    else:
        iterable = get_registered_actors().values()

    for definition, _ in iterable:
        names.add(definition.name)
        for chan in definition.inputs:
            get_chan(channels, chan)['consumers'].append(definition.name)

        for chan in definition.outputs:
            get_chan(channels, chan)['producers'].append(definition.name)

    edges = {}
    map(g.add_node, (pydot.Node(a, label=a) for a in names))
    for name, channel in channels.items():
        for consumer in channel['consumers']:
            for producer in channel['producers']:
                edges.setdefault((consumer, producer), []).append(name)
                g.add_edge(pydot.Edge(producer, consumer, label=name))

    return g


def dump_as_dot_graph(actors=None):
    return convert_to_graph(actors).to_string()
