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

    def test_group_actor(self):
        """ Load a group actor """
        load(self.actors_path, tags=['group_actor'])
        self.assertIsNotNone(get_actor('group_actor'))

    def test_no_executor_actor(self):
        """ Load an actor with no executor """
        with self.assertRaises(ValueError):
            load(self.actors_path, tags=['no_executor_actor'])
        self.assertIsNone(get_actor('no_executor_actor'))

    def test_load_actor_twice(self):
        """ Load an actor twice"""
        load(self.actors_path, tags=['load_twice_actor'])
        self.assertIsNotNone(get_actor('load_twice_actor'))
        with self.assertRaises(LookupError):
            load(self.actors_path, tags=['load_twice_actor'])

    def test_incomplete_actor(self):
        """ Load aa incomplete actor """
        with self.assertRaises(LookupError):
            load(self.actors_path, tags=['incomplete_group_actor'])
        self.assertIsNone(get_actor('incomplete_group_actor'))


if __name__ == '__main__':
    unittest.main()
