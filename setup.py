#!/usr/bin/env python3
"""
The foundation for this setup.py was taken from:

https://github.com/reillysiemens/layabout/blob/master/setup.py
"""
import re
import sys

from typing import IO


from setuptools import setup

if sys.version_info < (3, 6):
    sys.exit('Only Python 3.6+ is supported.')

from pathlib import Path


def get_version(path: IO) -> str:
    with open(path) as version_handle:
        return version_handle.read()


here = Path(__name__).cwd()
readme = (here / 'README.md').read_text()
version = get_version((here / 'VERSION'))

# Requirements.
install_reqs = [
    'jinja2'
]

test_reqs = [
    'black',
    'mypy',
    'pytest',
    'pytest-cov',
]

# TODO: Add these when we're ready to document things.
docs_reqs = [
    #'Sphinx',
    #'sphinx-autodoc-typehints',
]
dev_reqs = test_reqs + docs_reqs

setup(
    name='dragonstepsfire.com',
    version=version,
    description='The Dragonsteps performing arts group website.',
    long_description=readme,
    author='Alex LordThorsen, Kricket Keeling',
    author_email='AlexLordThorsen@gmail.com, KricketKeeling@gmail.com',
    url='https://github.com/DragonstepsFire/dragonstepsfire.com',
    install_requires=install_reqs,
    license='ISCL',
    py_modules=['render_site'],
    keywords='website arts',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    test_suite='tests',
    tests_require=test_reqs,
    python_requires='>=3.6',
    extras_require={
        'dev': dev_reqs,
        'docs': docs_reqs,
        'test': test_reqs,
    },
)

