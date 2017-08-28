import sys
import json
import shlex
from subprocess import Popen, PIPE


def _execute(cmd):
    return Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE).communicate()


def _build_cmd(source_path, name, img, init_bin, forward_ports):
    good_mounts = ['bin', 'etc', 'home', 'lib', 'lib64', 'media',
                   'opt', 'root', 'sbin', 'srv', 'usr', 'var']

    cmd = 'docker create --restart always -ti -v /sys/fs/cgroup:/sys/fs/cgroup:ro'

    for mount in good_mounts:
        cmd += ' -v {d}/{m}:/{m}:Z'.format(d=source_path, m=mount)

    for host_port, container_port in forward_ports:
        if host_port is None:
            cmd += ' -p {:d}'.format(container_port)  # docker will select random host_port
        else:
            cmd += ' -p {:d}:{:d}'.format(host_port, container_port)

    cmd += ' --name ' + name + ' ' + img + ' ' + init_bin

    return cmd


if __name__ == "__main__":
    inputs = json.load(sys.stdin)

    cmd = _build_cmd(inputs['container_dir'],
                     inputs['container_name'],
                     inputs['image'],
                     inputs['init_bin'],
                     forward_ports=inputs['forward_ports'])

    out, err = _execute(cmd)
    outputs = {
        'container_id': out or None,
        'error': err or None
    }
    print(json.dumps(outputs))
