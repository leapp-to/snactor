import pytest

from snactor.executors.default import Executor
from snactor.definition import Definition
from snactor.registry.schemas import get_schema, register_schema
from snactor.registry.actors import register_actor, get_registered_actors, get_actor, _clear_actors
from snactor.registry.envs import get_environment_extension, register_environment_variable
from snactor.registry.output_processors import get_output_processor, registered_output_processor
from snactor.registry.schemas import LATEST


@pytest.fixture(scope="module")
def actor_data():
    return (
        ('actor_name1', Definition('actor_name1', {'$location': './actor_name1/_actor.yaml'}), Executor),
        ('actor_name2', Definition('actor_name2', {'$location': './actor_name2/_actor.yaml'}), Executor),
        ('actor_name3', Definition('actor_name3', {'$location': './actor_name3/_actor.yaml'}), Executor)
    )


def test_actor_registration(actor_data):
    _clear_actors()
    for actor in actor_data:
        register_actor(actor[0], actor[1], actor[2])
        with pytest.raises(LookupError):
            register_actor(actor[0], actor[1], actor[2])

    assert get_registered_actors() == {x[0]: (x[1], x[2]) for x in actor_data}


def test_get_actor(actor_data):
    actor_name = actor_data[0][0]
    assert get_actor('non_existent_actor') is None
    assert isinstance(get_actor(actor_name), Executor)


def test_environment_variable_variables():
    data = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3'
    }

    for k, v in data.items():
        register_environment_variable(k, v)
        with pytest.raises(LookupError):
            register_environment_variable(k, v)

    assert get_environment_extension() == data


def test_schema_registration():
    definition1 = {
        'name': 'test1',
        'outputs': {},
        'inputs': {}
    }
    definition2 = {
        'name': 'test2',
        'outputs': {},
        'inputs': {}
    }

    # double insert
    register_schema('name1', LATEST, definition1)
    register_schema('name1', LATEST, definition1)

    # lookup error
    with pytest.raises(LookupError):
        register_schema('name1', LATEST, definition2)

    # retrieve
    assert get_schema('non_existent_name', LATEST) is None
    assert get_schema('name1', LATEST) == definition1
    assert get_schema('name1', "non_existing_version") is None


def test_output_processor_registration():
    definition1 = {
        'name': 'test1',
        'type': 'test_output_processor',
        'outputs': {},
        'inputs': {}
    }

    class TestOutputProcessorDefinition(object):
        def __init__(self, *args):
            pass

    @registered_output_processor('test_output_processor')
    class TestOutputProcessor(object):
        Definition = TestOutputProcessorDefinition

        def __init__(self, *args):
            pass

    assert get_output_processor('non_existent_output_processor') is None
    assert isinstance(get_output_processor(definition1), TestOutputProcessor)
