""" Inspect machine via ansible using snactor """
from generic_runner import run, pprint, get_actor


def inspect_machine_ansible():
    """ Run multiple checks at a given machine """
    machineinfo = {
        "source_host": [{"value": "localhost"}],
        "source_user_name": [{"value": "root"}],
    }
    get_actor('inspect_machine_ansible_group').execute(machineinfo)
    get_actor('inspect_machine').execute(machineinfo)
    pprint(machineinfo['machineinfo'])


if __name__ == '__main__':
    run(inspect_machine_ansible, tags=['inspect_machine'])
