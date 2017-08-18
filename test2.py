import snactor.executors
from snactor.loader import load
from snactor.registry import get_actor
from pprint import pprint
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
load('examples/actors')

data = {}
print get_actor('osversion')().execute(data)
pprint(data)
