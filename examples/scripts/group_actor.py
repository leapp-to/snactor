""" Sample script to test group executor """
from generic_runner import run, pprint, get_actor


def test_group_actor():
    """ Execute group-actor to test group executor """
    data = {}
    get_actor('group-actor').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(test_group_actor)
