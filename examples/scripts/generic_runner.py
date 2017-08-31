import logging
import os.path
import sys
from pprint import pprint

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(_BASE_DIR))

from snactor.loader import load, load_schemas, validate_actor_types, get_actor

def run(function, tags=()):
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    load(os.path.join(_BASE_DIR, 'actors'), tags=tags)
    load_schemas(os.path.join(_BASE_DIR, 'schema'))
    validate_actor_types()
    function()
