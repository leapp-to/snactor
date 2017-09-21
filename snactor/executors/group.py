from snactor.executors.default import Executor, registered_executor, filter_by_channel
from snactor.registry import must_get_actor


class GroupExecutorDefinition(Executor.Definition):
    def __init__(self, init):
        super(GroupExecutorDefinition, self).__init__(init)
        self.actors = map(must_get_actor, init.get('actors', ()))


@registered_executor('group')
class GroupExecutor(Executor):
    Definition = GroupExecutorDefinition

    def __init__(self, definition):
        super(GroupExecutor, self).__init__(definition)
        verify = set(i['name'] for i in definition.inputs)
        for actor in self.definition.executor.actors:
            actor_inputs = set(i['name'] for i in actor.definition.inputs)
            if actor.definition.inputs and not actor_inputs.issubset(verify):
                raise LookupError("Missing input available for actor ", actor.definition.name, "Missing:",
                                  actor_inputs - verify)
            [verify.add(i['name']) for i in actor.definition.outputs]

    def execute_remote(self, data, host, user):
        return self._execute(data, (host, user))

    def execute(self, data):
        return self._execute(data)

    def _execute(self, data, remote=None):
        restricted = filter_by_channel(self.definition.inputs, data)

        ret = True
        for actor in self.definition.executor.actors:
            if remote:
                ret = actor.execute_remote(restricted, *remote)
            else:
                ret = actor.execute(restricted)
            if not ret:
                break

        data.update(filter_by_channel(self.definition.outputs, restricted))

        return ret
