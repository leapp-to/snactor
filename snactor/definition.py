
class Definition(object):
    def __init__(self, name, init=None):
        init = init or {}
        self.name = name
        self.tags = set(init.get('tags', ()))
        self.inputs = init.get('inputs', ())
        self.outputs = init.get('outputs', ())
        if not isinstance(self.outputs, (list, tuple)):
            self.outputs = (self.outputs,)
        self.description = init.get('description', 'No description has been provided for this actor')
        self.executor = init.get('executor', None)
        self.extends = init.get('extends', None)
