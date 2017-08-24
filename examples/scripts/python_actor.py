""" Sample script to test python executor """
import logging
from pprint import pprint
from snactor.loader import load
from snactor.registry import get_actor


def test_python_executor():
    """ Execute osversion actor to test python executor """
    data = {}
    get_actor('osversion')().execute(data)
    pprint(data)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    load('../actors')
    test_python_executor()
