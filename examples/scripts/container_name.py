""" Sample script to test create_container_name actor """
from generic_runner import run, pprint, get_actor


def test_create_container_name_actor():
    data = {'user_container_name': [{'value': ''}], 'hostnameinfo': [{'hostname': 'test_hostname'}]}
    get_actor('create_container_name').execute(data)
    pprint(data)
    data = {'user_container_name': [{'value': 'test'}], 'hostnameinfo': [{'hostname': 'test_hostname'}]}
    get_actor('create_container_name').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(test_create_container_name_actor)
