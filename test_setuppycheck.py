import os

import pytest

from scripttest import TestFileEnvironment

here = os.path.realpath(os.path.dirname(__file__))


@pytest.fixture
def env():
    return TestFileEnvironment()


@pytest.fixture
def venv(env):
    def setuppycheck(*args, **kwargs):
        return env.run(
            os.path.join(env.virtualenv_bin_dir, 'setuppycheck'),
            *args, **kwargs)

    env.run('virtualenv', 'venv')
    env.virtualenv_dir = os.path.join(env.base_path, 'venv')
    env.virtualenv_bin_dir = os.path.join(env.virtualenv_dir, 'bin')
    pip = os.path.join(env.virtualenv_bin_dir, 'pip')
    env.run(pip, 'install', '-e', here)
    env.setuppycheck = setuppycheck
    return env


def test_reads_requirements_txt(venv):
    setuppy = os.path.join(here, 'examples/reads_requirements_text/setup.py')
    ret = venv.setuppycheck(setuppy, expect_error=True)
    assert ret.returncode == 1
    assert 'looks like a requirements file?' in ret.stderr
    assert 'https://caremad.io/2013/07/setup-vs-requirement/' in ret.stderr


def test_exact_pins(venv):
    setuppy = os.path.join(here, 'examples/exact_pins/setup.py')
    ret = venv.setuppycheck(setuppy, expect_error=True)
    assert ret.returncode == 1
    assert "WARNING: exact pin: 'requests==2.7.0'" in ret.stderr
