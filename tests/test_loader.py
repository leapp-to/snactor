#!/usr/bin/env python
""" Unit tests related with snactor's actor loading """
import os
import unittest
from snactor.loader import load
from snactor.registry import get_actor


class TestLoader(unittest.TestCase):
    """ Loader test case """
    def __init__(self, *args, **kwargs):
        super(TestLoader, self).__init__(*args, **kwargs)

        basedir = os.path.dirname(os.path.abspath(__file__))
        self.actors_path = os.path.join(basedir, 'actors')

    def test_simple_actor(self):
        """ Load a simple actor """
        load(self.actors_path, tags=['simple_actor'])
        self.assertIsNotNone(get_actor('simple_actor'))

    def test_extends_executor_actor(self):
        """ Load an actor with both extends and executor """
        with self.assertRaises(ValueError):
            load(self.actors_path, tags=['extends_executor_actor'])
        self.assertIsNone(get_actor('extends_executor_actor'))

    def test_extends_no_actor(self):
        """ Load an actor that extends a non-existent actor """
        with self.assertRaises(LookupError):
            load(self.actors_path, tags=['extends_no_actor'])
        self.assertIsNone(get_actor('extends_no_actor'))


if __name__ == '__main__':
    unittest.main()
