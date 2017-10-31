""" Inspect machine via ansible using snactor """
from generic_runner import run, pprint, get_actor


def remote_target_check():
    """ Run multiple checks at a given machine """
    data = {
        "target_host": [{"value": "10.34.76.245"}],
        "target_user_name": [{"value": "root"}],
        "container_name": [{"value": "container_centos6-app-vm"}]
    }
    get_actor('remote-destroy-container').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(remote_target_check)
