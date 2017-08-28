from snactor.executors.default import ExecutorDefinition
from snactor.registry import must_get_actor
from snactor.utils.variables import resolve_variable_spec


class ExtendsActorDefinition(ExecutorDefinition):
    def __init__(self, init):
        self.extended = init['extended']
        self.required_inputs = init.get('inputs', ())
        self.inputs = init.get('extends', {}).get('inputs', ())
        self.output = init.get('extends', {}).get('outputs', ())
        self.restricted_inputs = [i['name'] for i in self.extended.inputs]


class ExtendsActor(object):
    Definition = ExtendsActorDefinition

    def __init__(self, definition):
        self.definition = definition

    def execute(self, data):
        extends = ExtendsActorDefinition(self.definition)
        restricted = {n['name']: data[n['name']] for n in extends.required_inputs}
        restricted.update({
            i['name']: resolve_variable_spec(restricted, i['source'])
            for i in extends.inputs if 'source' in i
        })
        restricted.update({i['name']: i['value'] for i in extends.inputs if 'value' in i})

        actor = must_get_actor(self.definition['extended'].name)
        ret = actor.execute(restricted)
        if ret:
            for output in extends.output:
                data[output['name']] = resolve_variable_spec(restricted, output['source'])

        return ret
