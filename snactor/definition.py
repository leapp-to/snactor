import yaml


class Definition(object):
    def __init__(self, name, init=None):
        init = init or {}
        self.name = name
        self.inputs = init.get('inputs', ())
        self.output = init.get('output')
        self.schemas = init.get('schemas', {})
        self.description = init.get('description', 'No description has been provided for this actor')
        self.execute = init.get('execute', None)
        self.payload = init.get('payload', None)
        self.type = init.get('type', 'simple')

    @classmethod
    def from_file(cls, name, path):
        with open(path, 'r') as f:
            return cls(name, yaml.load(f))
