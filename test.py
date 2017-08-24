""" Sample script to test simple executor """
import logging
from pprint import pprint
from snactor.loader import load
from snactor.registry import get_actor


def test_simple_actor():
    """ Execute simple-actor to test simple executor """
    data = {}
    get_actor('simple-actor')().execute(data)
    pprint(data)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    load('examples/actors')
    test_simple_actor()
