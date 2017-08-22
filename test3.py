import snactor.executors
from snactor.loader import load
from snactor.registry import get_actor
from pprint import pprint
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
load('examples/actors', tags=['packages'])

data = {
    "filter": {"value": "test"},
    "rpm_packages": {
        "packages": [{
            "name": "test-1",
            "version": "1"},{
            "name": "tast-2",
            "version": "1"},{
            "name": "test-3",
            "version": "1"},{
            "name": "tast-1",
            "version": "1"}]}}
print get_actor('filter_packages')().execute(data)
pprint(data)
