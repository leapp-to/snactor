import imp
import importlib
import os

_IMPORTED = set()


def from_package(name):
    if name in _IMPORTED:
        return
    _IMPORTED.add(name)
    package = importlib.import_module(name)
    for _, _, files in os.walk(package.__path__[0]):
        for f in files:
            if f.endswith('.py') and f != '__init__.py':
                importlib.import_module('.' + os.path.splitext(f)[0], name)


def from_directory(path):
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.py') and f != '__init__.py':
                modname = os.path.splitext(f)[0]
                f, filename, description = imp.find_module(modname, [root])
                imp.load_module(modname, f, filename, description)
