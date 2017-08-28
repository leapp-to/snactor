""" Sample script to test extended actor """
import logging
from pprint import pprint
from snactor.loader import load
from snactor.registry import get_actor


def test_extended_actor():
    """ Execute filter_kernel_packages actor to test extended actor """
    data = {
        "rpm_packages": {
            "packages": [
                {"name": "test-1", "version": "1"},
                {"name": "kernel-2", "version": "1"},
                {"name": "test-3", "version": "1"},
                {"name": "kernel-1", "version": "1"}
            ]
        }
    }

    print("Before execution")
    print("=" * 70)
    pprint(data)
    print("=" * 70)
    print("Execution result:",
          get_actor('filter_kernel_packages').execute(data))
    print("=" * 70)
    print("After execution")
    pprint(data)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    load('../actors')
    test_extended_actor()
