#!/usr/bin/env python

import __builtin__
import logging
import mock
import sys

level = logging.INFO
# level = logging.DEBUG
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

orig_open = __builtin__.open


def setup(**kwargs):
    install_requires = kwargs.get('install_requires')
    logger.debug('install_requires = %r' % install_requires)

    for req in install_requires:
        if '==' in req:
            sys.stderr.write(
                'WARNING: exact pin: %r\n' % req)


def open(name, **kwargs):
    logger.debug('open: %s', name)

    if 'requirements' in name:
        sys.stderr.write(
            'WARNING: reads %r - looks like a requirements file?\n'
            % name)
        sys.stderr.write(
            '  You might want to look at '
            'https://caremad.io/2013/07/setup-vs-requirement/\n')

    return orig_open(name, **kwargs)


def setuppycheck(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    for setuppy in argv:
        with mock.patch('setuptools.setup', side_effect=setup):
            with mock.patch('__builtin__.open', side_effect=open):
                execfile(setuppy, globals())


if __name__ == '__main__':
    setuppycheck()
