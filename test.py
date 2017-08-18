import logging
import yaml
from snactor.executors.default import Executor, Definition
import sys
from pprint import pprint

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
a = yaml.load(open('examples/actors/simple-actor.yaml'))
d = Definition('simple-actor', a)
d.executor = Executor.Definition(d.executor)
e = Executor(d)
data = {}
result = e.execute(data)

print result
pprint(data)
