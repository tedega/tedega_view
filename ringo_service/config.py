#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Service configuration
See http://flask.pocoo.org/docs/0.12/config/
"""


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    API_CONFIG = '../swagger/api.yaml'
    SERVER = 'gevent'
    SERVER_PORT = 8080


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:///db.sqlite'
    DEBUG = True
    SERVER = None


class TestingConfig(Config):
    TESTING = True
