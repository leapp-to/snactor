""" Sample script to test output processors """
import logging
from pprint import pprint
from snactor.loader import load
from snactor.registry import get_actor


def test_output_processors():
    """ Execute iplist actor to test output processors """
    data = {}
    print("Before execution")
    print("=" * 70)
    pprint(data)
    print("=" * 70)
    print("Execution result:",
          get_actor('iplist')().execute(data))
    print("=" * 70)
    print("After execution")
    pprint(data)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    load('../actors')
    test_output_processors()
