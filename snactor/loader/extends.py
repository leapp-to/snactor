from snactor.executors.default import filter_by_channel
from snactor.definition import Definition
from snactor.registry import must_get_actor
from snactor.utils.variables import resolve_variable_spec


class ExtendsActorDefinition(Definition):
    def __init__(self, name, init):
        super(ExtendsActorDefinition, self).__init__(init)
        self.name = name
        self.extended = init['extended']
        self.extended_inputs = init.get('extends', {}).get('inputs', ())
        self.extended_outputs = init.get('extends', {}).get('outputs', ())
        self.restricted_inputs = [i['name'] for i in self.inputs]


class ExtendsActor(object):
    Definition = ExtendsActorDefinition

    def __init__(self, definition):
        self.definition = definition

    def execute(self, data):
        restricted = filter_by_channel(self.definition.required_inputs, data)
        restricted.update({
            i['name']: resolve_variable_spec(restricted, i['source'])
            for i in self.definition.inputs if 'source' in i
        })
        restricted.update({i['name']: i['value'] for i in self.definition.inputs if 'value' in i})

        actor = must_get_actor(self.definition.name)
        ret = actor.execute(restricted)
        if ret:
            for output in self.definition.outputs:
                restricted[output['name']] = resolve_variable_spec(restricted, output['source'])
            data.update(filter_by_channel(self.definition.outputs, restricted))

        return ret
