""" Sample script to test passing data to an actor """
from generic_runner import run, pprint, get_actor


def test_passing_data_actor():
    """ Execute  actor providing data"""
    data = {
        "filter": [{"value": "test"}],
        "rpm_packages": [{
            "packages": [
                {"name": "test-1", "version": "1"},
                {"name": "tast-2", "version": "1"},
                {"name": "test-3", "version": "1"},
                {"name": "tast-1", "version": "1"}
                ]
            }]
    }
    get_actor('filter_packages').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(test_passing_data_actor, tags=['packages'])
