# -*- coding: utf-8 -*-

from .registry import (
    config_view_endpoint
)
from .exceptions import (
    NotFound,
    ClientError,
    AuthError
)
from .service import start_service

__all__ = [config_view_endpoint,
           NotFound, ClientError, AuthError,
           start_service]

__author__ = """Torsten Irländer"""
__email__ = 'torsten.irlaender@googlemail.com'
__version__ = '0.1.0'