""" Run target checks using snactor """
import logging
from pprint import pprint
from snactor.loader import load
from snactor.registry import get_actor


def check_target():
    """ Run multiple checks at target machine """
    targetinfo = {}
    get_actor('check_target_group').execute(targetinfo)

    get_actor('check_target').execute(targetinfo)
    pprint(targetinfo['targetinfo'])


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO)
    load('../actors', tags=['check_target'])
    check_target()
