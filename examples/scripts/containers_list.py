""" Sample script to test simple executor """
from generic_runner import run, pprint, get_actor


def test_simple_actor():
    """ Execute containers_list to test simple executor """
    data = {}
    get_actor('containers_list').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(test_simple_actor)
