from ..registry import registered_output_processor
from ..utils.variables import assign_to_variable_spec


class StringListOutputProcessorDefinition(object):
    def __init__(self, init):
        self.target = init.get('target', None)


@registered_output_processor('string-list')
class StringListOutputProcessor(object):
    Definition = StringListOutputProcessorDefinition

    def __init__(self, definition):
        self.definition = definition

    def process(self, output, data):
        assign_to_variable_spec(data, self.definition.target, output.split('\n'))
