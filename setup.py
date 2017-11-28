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
    name='tedega_service',
    version='0.1.0',
    description="Tedega service",
    long_description=readme + '\n\n' + history,
    author="Torsten Irländer",
    author_email='torsten.irlaender@googlemail.com',
    url='https://github.com/toirl/tedega_service',
    packages=[
        'tedega_service',
    ],
    package_dir={'tedega_service':
                 'tedega_service'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='tedega_service',
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
