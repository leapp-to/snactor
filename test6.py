import snactor.executors
from snactor.loader import load
from snactor.registry import get_actor
from pprint import pprint
import logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
load('examples/actors')

data = {}
print "Before execution"
print "======================================================================="
pprint(data)
print "======================================================================="
print "Execution result:", get_actor('ansible_setup')().execute(data)
print "======================================================================="
print "After execution"
pprint(data)

