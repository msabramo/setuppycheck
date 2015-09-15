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
output_format = 'text'
setup_vs_requirement_link = 'https://caremad.io/2013/07/setup-vs-requirement/'


def link(url):
    return '<a href="%(url)s">%(url)s</a>' % {'url': url}


class ExactPinWarning(object):
    def __init__(self, req):
        self.req = req

    def emit(self, output_file, output_format):
        if output_format == 'html':
            output_file.write(
                '<li>WARNING: exact pin: %r</li>\n' % self.req)
        else:
            output_file.write(
                'WARNING: exact pin: %r\n' % self.req)


class ReadsRequirementsFileWarning(object):
    def __init__(self, name):
        self.name = name

    def emit(self, output_file, output_format='text'):
        if output_format == 'html':
            output_file.write(
                '<li>WARNING: reads %s - '
                'looks like a requirements file?<br/>\n'
                % self.name)
            output_file.write(
                '    You might want to look at %s</li>\n'
                % link(setup_vs_requirement_link))
        else:
            output_file.write(
                'WARNING: reads %s - '
                'looks like a requirements file?\n'
                % self.name)
            output_file.write(
                '    You might want to look at %s\n'
                % setup_vs_requirement_link)


def setup(**kwargs):
    global is_setuppy_ok, output_format

    install_requires = kwargs.get('install_requires')
    logger.debug('install_requires = %r' % install_requires)

    for req in install_requires:
        if '==' in req:
            ExactPinWarning(req).emit(warnings_output_file, output_format)
            is_setuppy_ok = False


def open(name, **kwargs):
    global is_setuppy_ok, output_format

    logger.debug('open: %s', name)

    if 'requirements' in name:
        ReadsRequirementsFileWarning(name).emit(
            warnings_output_file, output_format)
        is_setuppy_ok = False

    return orig_open(name, **kwargs)


@click.command()
@click.argument('setuppy_file_paths', nargs=-1)
@click.option('--output-format',
              type=click.Choice(['text', 'html']), default='text',
              help='Output warnings in HTML')
def setuppycheck(output_format, setuppy_file_paths):
    globals()['output_format'] = output_format

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

    exit_code = 0 if is_setuppy_ok else 1
    sys.exit(exit_code)


if __name__ == '__main__':
    setuppycheck()
