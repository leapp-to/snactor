from snactor.loader import load
from snactor.utils.auto_loader import from_package
from snactor.registry import get_actor
from pprint import pprint
import logging

from_package('snactor.executors')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
load('examples/actors')

data = {
    #    "filter": {"value": "test"},
    "rpm_packages": {
        "packages": [{
            "name": "test-1",
            "version": "1"},{
            "name": "kernel-2",
            "version": "1"},{
            "name": "test-3",
            "version": "1"},{
            "name": "kernel-1",
            "version": "1"}]}}
print "Before execution"
print "======================================================================="
pprint(data)
print "======================================================================="
print "Execution result:", get_actor('filter_kernel_packages')().execute(data)
print "======================================================================="
print "After execution"
pprint(data)
