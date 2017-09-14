from distutils.core import setup
from setuptools import find_packages

setup(
    name='snactor',
    version='0.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    url='https://github.com/leapp-to/snactor',
    license='ASL 2.0',
    author="Vinzenz 'evilissimo' Feenstra",
    author_email='evilissimo@redhat.com',
    description='snactor is a python library for actors',
    install_requires=['PyYAML', 'jsl', 'argcomplete', 'jsonschema', 'six']
)
