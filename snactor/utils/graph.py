from snactor.registry import get_registered_actors
from snactor.utils import get_chan

try:
    import pydot
except ImportError:
    pydot = None


def convert_to_graph(actors=None):
    """
    :param actors: List of actors or None. In case this is None or empty the graph will be generated from all loaded
                   actors
    :return: A pydot.Graph instance representing the actor dependency graph
    """
    if not pydot:
        raise Exception("Please install pydot before you use the snactor graph support")

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
    """
    :param actors: List of actors or None. In case this is None or empty the graph will be generated from all loaded
                   actors
    :return: A string in the dot graph format
    """
    return convert_to_graph(actors).to_string()
