
class Definition(object):
    def __init__(self, name, init=None):
        init = init or {}
        self.name = name
        self.inputs = init.get('inputs', ())
        self.output = init.get('output', ())
        if not isinstance(self.output, (list, tuple)):
            self.output = (self.output,)
        self.description = init.get('description', 'No description has been provided for this actor')
        self.executor = init.get('executor', None)
        self.extends = init.get('extends', None)
