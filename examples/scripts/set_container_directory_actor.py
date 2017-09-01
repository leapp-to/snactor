""" Sample script to test set_container_dir actor """
from generic_runner import run, pprint, get_actor


def test_set_container_directory_actor():
    # data = {'container_name': {'value': 'container-name_name8'}}
    data = {'container_name': {'value': 'a'}}
    get_actor('set_container_directory').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(test_set_container_directory_actor)
