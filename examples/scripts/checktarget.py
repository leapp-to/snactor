""" Run target checks using snactor """
from generic_runner import run, pprint, get_actor


def check_target():
    """ Run multiple checks at target machine """
    targetinfo = {}
    get_actor('check_target_group').execute(targetinfo)

    get_actor('check_target').execute(targetinfo)
    pprint(targetinfo['targetinfo'])


if __name__ == '__main__':
    run(check_target, tags=['check_target'])
