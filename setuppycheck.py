#!/usr/bin/env python

__author__ = 'Marc Abramowitz'
__version__ = '0.0.0'

import __builtin__
import logging
import mock
import os
import pprint
import sys

level = logging.INFO
# level = logging.DEBUG
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

orig_open = __builtin__.open
is_setuppy_ok = True


def setup(**kwargs):
    global is_setuppy_ok

    install_requires = kwargs.get('install_requires')
    logger.debug('install_requires = %r' % install_requires)

    for req in install_requires:
        if '==' in req:
            sys.stderr.write(
                'WARNING: exact pin: %r\n' % req)
            is_setuppy_ok = False


def open(name, **kwargs):
    global is_setuppy_ok

    logger.debug('open: %s', name)

    if 'requirements' in name:
        sys.stderr.write(
            'WARNING: reads %r - looks like a requirements file?\n'
            % name)
        sys.stderr.write(
            '  You might want to look at '
            'https://caremad.io/2013/07/setup-vs-requirement/\n')
        is_setuppy_ok = False

    return orig_open(name, **kwargs)


def setuppycheck(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    for setuppy in argv:
        setuppy = os.path.realpath(setuppy)

        with mock.patch('setuptools.setup', side_effect=setup):
            with mock.patch('__builtin__.open', side_effect=open):
                os.chdir(os.path.dirname(setuppy))
                execfile(setuppy, globals())

    return 0 if is_setuppy_ok else 1


if __name__ == '__main__':
    sys.exit(setuppycheck())
