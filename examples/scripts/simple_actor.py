""" Sample script to test simple executor """
from generic_runner import run, pprint, get_actor


def test_simple_actor():
    """ Execute simple-actor to test simple executor """
    data = {}
    get_actor('simple-actor').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(test_simple_actor)
