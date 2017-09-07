#!/usr/bin/env python
""" Build and run workflow using LeApp Workflow module """
from pprint import pprint

from generic_runner import wf_run


def process_result(wfresult):
    pprint(wfresult['targetinfo'].pop().payload)

if __name__ == '__main__':
    wf_run('check_target', process_result, tags=('check_target',))