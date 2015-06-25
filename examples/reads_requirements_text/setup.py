import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def get_requirements(fn):
    reqs = [str(i.strip())
            for i in open(os.path.join(here, fn))
            if not i.startswith(('#', '-'))]
    reqs = [req
            for req in reqs
            if req]
    return reqs


setup(
    name='myapp',
    version='0.0.0',
    install_requires=get_requirements('requirements.txt'),
)
