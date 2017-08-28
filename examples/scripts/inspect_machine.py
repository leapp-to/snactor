""" Inspect machine using snactor """
import logging
from pprint import pprint
from snactor.loader import load
from snactor.registry import get_actor


def inspect_machine(shallow=True):
    """ Run multiple checks at target machine """
    machineinfo = {}
    get_actor('inspect_machine_group').execute(machineinfo)
    if not shallow:
        get_actor('rpm_list').execute(machineinfo)
    get_actor('inspect_machine').execute(machineinfo)
    pprint(machineinfo['machineinfo'])


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO)
    load('../actors', tags=['inspect_machine'])
    inspect_machine()
