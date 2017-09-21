#!/usr/bin/env python
""" Execute an actor using snactor """
import json
import logging
import os
import sys
from argparse import ArgumentParser

from snactor.loader import load, load_schemas, validate_actor_types, get_actor

__version__ = '0.0.1'


def parse_arguments():
    """ Define and process cli arguments """
    parser = ArgumentParser()

    parser.add_argument("actor",
                        help="execute actor",
                        type=str)

    parser.add_argument('--actors_dir',
                        default=None,
                        help="path containing actor(s) definition")

    parser.add_argument('--schemas_dir',
                        default=None,
                        help="path containing schema(s) definition")

    parser.add_argument('--validate',
                        action='store_true',
                        default=False,
                        help="validate loaded actors and schemas")

    parser.add_argument('-v', '--version',
                        action='version',
                        version=__version__,
                        help='display version information')

    return parser.parse_args()


def load_actors(actors_dir, schemas_dir):
    """ Load and validade actors and schemas """
    if not actors_dir:
        actors_dir = os.getcwd()

    if not schemas_dir:
        schemas_dir = os.getcwd()

    logging.debug("Loading actors definition: %s", actors_dir)
    load(actors_dir)
    logging.debug("Loading schemas definition: %s", schemas_dir)
    load_schemas(schemas_dir)


def main():
    """ Execute actor passing and retrieving data"""
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    args = parse_arguments()

    load_actors(args.actors_dir, args.schemas_dir)
    if args.validate:
        logging.debug("Validating actors/schemas")
        validate_actor_types()

    data = {}
    if not sys.stdin.isatty():
        logging.debug("Reading input data from stdin")
        try:
            data = json.load(sys.stdin)
        except ValueError as err:
            logging.error("Unable to load input data: %s", err)
            sys.exit(1)

    actor = get_actor(args.actor)
    if not actor:
        logging.error("Unable to find actor: %s", args.actor)
        sys.exit(1)

    actor.execute(data)
    print(json.dumps(data))


if __name__ == '__main__':
    main()
