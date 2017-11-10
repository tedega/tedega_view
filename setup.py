#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'future',
    'connexion',
    'venusian',
    'flask_cors',
    'voorhees',
    'pytest-flask'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ringo_service',
    version='0.1.0',
    description="Ringo service",
    long_description=readme + '\n\n' + history,
    author="Torsten Irländer",
    author_email='torsten.irlaender@googlemail.com',
    url='https://github.com/toirl/ringo_service',
    packages=[
        'ringo_service',
    ],
    package_dir={'ringo_service':
                 'ringo_service'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='ringo_service',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
