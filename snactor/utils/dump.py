from collections import OrderedDict
import yaml

try:
    str_type = unicode
except NameError:
    str_type = str


class _UnsortableList(list):
    def sort(self, *args, **kwargs):
        pass


class _UnsortableOrderedDict(OrderedDict):
    def items(self, *args, **kwargs):
        return _UnsortableList(OrderedDict.items(self, *args, **kwargs))


class _LiteralUnicode(str_type):
    pass


def _literal_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


def _replacer(o):
    order = ['tags', 'inputs', 'outputs', 'description', 'execute', 'group']
    return _UnsortableOrderedDict([(k, _inner_replacer(o[k])) for k in order if k in o])


def _inner_replacer(o):
    if isinstance(o, dict):
        return {k: _inner_replacer(v) for k, v in o.items()}
    if isinstance(o, str):
        if '\n' in o:
            return _LiteralUnicode(o)
    return o


def dump_group_to_yaml(group_actor):
    d = {'group': group_actor.definition.init.get("group", ())}
    if group_actor.definition.inputs:
        d['inputs'] = group_actor.definition.inputs
    if group_actor.definition.outputs:
        d['outputs'] = group_actor.definition.outputs
    if group_actor.definition.tags:
        d['tags'] = group_actor.definition.tags
    if group_actor.definition.description:
        d['description'] = group_actor.definition.description
    return yaml.dump(_replacer(d), default_flow_style=False)


yaml.add_representer(_UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)
yaml.add_representer(_LiteralUnicode, _literal_unicode_representer)
