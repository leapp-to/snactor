import logging
import os.path
import sys
from pprint import pprint  # noqa

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(_BASE_DIR))

from snactor.loader import load, load_schemas, validate_actor_types, get_actor  # noqa


def run(fun, tags=()):
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    load(os.path.join(_BASE_DIR, 'actors'), tags=tags)
    load_schemas(os.path.join(_BASE_DIR, 'schema'))
    validate_actor_types()
    fun()
