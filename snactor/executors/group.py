from snactor.executors.default import Executor, filter_by_channel


class GroupExecutor(Executor):
    def __init__(self, definition):
        super(GroupExecutor, self).__init__(definition)
        verify = set(i['name'] for i in definition.inputs)
        for actor in self.definition.actors:
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
        sync_repo = True
        for actor in self.definition.actors:
            if remote:
                ret = actor.execute_remote(restricted, *remote, sync_repo=sync_repo)
                sync_repo = False
            else:
                ret = actor.execute(restricted)
            if not ret:
                break

        data.update(filter_by_channel(self.definition.outputs, restricted))

        return ret
