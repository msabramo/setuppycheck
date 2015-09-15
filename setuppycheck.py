#!/usr/bin/env python

__author__ = 'Marc Abramowitz'
__version__ = '0.0.1'

import __builtin__
import logging
import mock
import os
import sys

import click

level = logging.INFO
# level = logging.DEBUG
logging.basicConfig(level=level)
logger = logging.getLogger(__name__)

orig_open = __builtin__.open
is_setuppy_ok = True
warnings_output_file = sys.stderr


def setup(**kwargs):
    global is_setuppy_ok

    install_requires = kwargs.get('install_requires')
    logger.debug('install_requires = %r' % install_requires)

    for req in install_requires:
        if '==' in req:
            warnings_output_file.write(
                'WARNING: exact pin: %r\n' % req)
            is_setuppy_ok = False


def open(name, **kwargs):
    global is_setuppy_ok

    logger.debug('open: %s', name)

    if 'requirements' in name:
        warnings_output_file.write(
            'WARNING: reads %s - looks like a requirements file?\n'
            % name)
        warnings_output_file.write(
            '  You might want to look at '
            'https://caremad.io/2013/07/setup-vs-requirement/\n')
        is_setuppy_ok = False

    return orig_open(name, **kwargs)


@click.command()
@click.argument('setuppy_file_paths', nargs=-1, required=True)
def setuppycheck(setuppy_file_paths):
    for setuppy in setuppy_file_paths:
        setuppy = os.path.realpath(setuppy)

        with mock.patch('setuptools.setup', side_effect=setup):
            with mock.patch('__builtin__.open', side_effect=open):
                # Override __file__ that setup.py receives
                #
                # If called as a console_script, we want the setup.py to
                # receive a __file__ that points to setup.py; not setupcheck.py
                #
                # Otherwise if the setup.py does something like:
                #
                #     here = os.path.abspath(os.path.dirname(__file__))
                #
                # it will get the wrong directory and chaos will ensue.
                #
                execfile_globals = globals().copy()
                execfile_globals['__file__'] = setuppy

                os.chdir(os.path.dirname(setuppy))
                execfile(setuppy, execfile_globals)

    return 0 if is_setuppy_ok else 1
