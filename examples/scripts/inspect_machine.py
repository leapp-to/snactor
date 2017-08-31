""" Inspect machine using snactor """
from generic_runner import run, pprint, get_actor


def inspect_machine(shallow=True):
    """ Run multiple checks at target machine """
    machineinfo = {}
    get_actor('inspect_machine_group').execute(machineinfo)
    if not shallow:
        get_actor('rpm_list').execute(machineinfo)
    get_actor('inspect_machine').execute(machineinfo)
    pprint(machineinfo['machineinfo'])


if __name__ == '__main__':
    run(inspect_machine, tags=['inspect_machine'])
