from subprocess import PIPE, Popen
from .executors.default import Definition


def execute(definition):
    if not isinstance(definition, Definition):
        raise ValueError("Invalid parameter - Expected a Definition")

    p = Popen(definition.execute, stdin=PIPE)
    if definition.payload:
        p.stdin.write(definition.payload)
    p.stdin.close()
    p.wait()

