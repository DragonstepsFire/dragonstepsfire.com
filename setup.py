"""Setup script for firelightcircus.com"""

import os
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

def load_requirements(path):
    with open(path) as handle:
        raw_reqs = handle.read().strip().split('\n')
        reqs = [req.split('/')[-2] if req.startswith('https://artifactory.eng.esentire.com') else req for req in raw_reqs]
        return reqs

def load_version():
    with open('VERSION') as handle:
        return handle.read()

requirements = load_requirements("requirements.txt")
test_requirements = load_requirements("requirements_dev.txt")
# TODO: Eventually add a docs requirements file when we have docs targets.

dev_requirements = test_requirements

setup(
    author="AlexLordThorsen",
    author_email="firelightcircus@gmail.com",
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Media and information for Firelight Circus.",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    package_data={'publisher': ['VERSION'],},
    keywords='firelightcirucs',
    name='firelightcircus',
    packages=find_packages(include=['publisher']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/DragonstepsFire/firelightcircus.com',
    version=load_version(),
    zip_safe=True,
    extras_require={
        'dev': dev_requirements,
        'test': test_requirements,
    },
)
