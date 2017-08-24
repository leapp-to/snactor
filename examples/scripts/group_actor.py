""" Sample script to test group executor """
import logging
from pprint import pprint
from snactor.loader import load
from snactor.registry import get_actor


def test_group_actor():
    """ Execute group-actor to test group executor """
    data = {}
    get_actor('group-actor')().execute(data)
    pprint(data)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    load('../actors')
    test_group_actor()
