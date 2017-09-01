""" Sample script to test create_container actor """
from generic_runner import run, pprint, get_actor


def test_create_container_actor():
    data = {
        'container_directory': {'value': '/var/lib/leapp/macrocontainers/cos7'},
        'container_name': {'value': 'cos7'},
        'image': {'value': 'centos:7'},
        'init_bin': {'value': '/sbin/init'},
        'exposed_ports': {
            'ports': [
                {'protocol': 'tcp', 'port': 22},
                {'protocol': 'tcp', 'port': 80, 'exposed_port': 8080},
                {'protocol': 'udp', 'port': 80, 'exposed_port': 8080},
            ]
        },
    }
    get_actor('create_container').execute(data)
    pprint(data)


if __name__ == '__main__':
    run(test_create_container_actor)
