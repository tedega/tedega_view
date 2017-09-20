#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Service configuration
See http://flask.pocoo.org/docs/0.12/config/
"""


class Config(object):
    DEBUG = False
    """Set to true to enable debug logging"""
    DATABASE_URI = 'sqlite://:memory:'
    """Configure the database connection."""
    API_CONFIG = '../swagger/api.yaml'
    """Path to the API configuration used by connexion."""
    DOMAIN_MODEL = ''
    """Path to the root class of your domain mode. E.g.
    `path.to.your.domain.Class`."""
    SERVER = 'gevent'
    """Configure which server should be used. Default to werkzeug."""
    SERVER_PORT = 8080
    """Configure the port on which the server will listen."""


class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///db.sqlite'


class DevelopmentConfig(Config):
    DATABASE_URI = 'sqlite:///db.sqlite'
    DEBUG = True
    SERVER = None
