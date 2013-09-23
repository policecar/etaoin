#! /usr/bin/env python

from setuptools import setup

setup(
    name='get-user-timeline',
    version='0.1',
    description='Retrieve Twitter user timeline and save tweets to file.',
    install_requires=[ 'argparse', 'oauth2' ]
)

