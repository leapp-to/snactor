import logging
import os.path
import sys
from pprint import pprint  # noqa

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(_BASE_DIR))

from snactor.loader import load, load_schemas, validate_actor_types, get_actor, get_registered_actors  # noqa


def actor_names_by_tags(tags, names=None):
    if names is None:
        return [name for name, a in get_registered_actors().items() if a[0].tags.intersection(tags)]
    else:
        return [name for name, a in get_registered_actors().items() if a[0].tags.intersection(tags) and name in names]


def run(fun, tags=()):
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    load(os.path.join(_BASE_DIR, 'actors'), tags=tags)
    load_schemas(os.path.join(_BASE_DIR, 'schema'))
    validate_actor_types()
    fun()


def wf_run(final_actor, fun, tags=()):
    def wf_construct_run():
        import leappwf
        wf = leappwf.Workflow()
        wf.load_snactors(names=actor_names_by_tags(tags=('depsolver',)))
        wf.complete()
        wf.prepare()
        # TODO it would be better to determine final_actor programmatically
        # TODO we should allow multiple final actors
        wfresult = wf.run(final_actor)
        fun(wfresult)

    run(wf_construct_run, tags)
