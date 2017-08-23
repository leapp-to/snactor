""" Run target checks using snactor """
import logging
from pprint import pprint
from snactor.loader import load
from snactor.registry import get_actor


def checktarget():
    """ Run multiple checks at target machine """
    actors = {'check-rsync': {},
              'check-docker': {},
              'check-containers-list': {}}

    for actor, data in actors.items():
        get_actor(actor)().execute(data)

    targetinfo = {}
    for data in actors.values():
        targetinfo.update(data)

    get_actor('check-target')().execute(targetinfo)
    pprint(targetinfo['targetinfo'])


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO)
    load('examples/actors', tags=['checktarget'])
    checktarget()
