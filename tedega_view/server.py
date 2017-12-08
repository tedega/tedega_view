#!/usr/bin/env python3
import os
import importlib
import venusian
from flask_cors import CORS
import connexion
from tedega_share import monitor_system

from .registry import registry
from .views import ViewResolver


def register_endpoints(modul):
    # Scan for service endpoints and models in the given modul and store
    # these in the registry.
    scanner = venusian.Scanner(registry=registry)
    scanner.scan(modul)


def create_server(modul, swagger_file):
    package_directory = os.path.dirname(os.path.abspath(modul.__file__))
    swagger = os.path.abspath(os.path.join(package_directory, swagger_file))
    connexion_app = connexion.App(__name__)
    connexion_app.add_api(swagger, resolver=ViewResolver())
    CORS(connexion_app.app)
    return connexion_app


def start_server(modulname, swagger_file="swagger.yaml", port=None, server=None):
    modul = importlib.import_module(modulname)
    register_endpoints(modul)
    connexion_app = create_server(modul, swagger_file)
    config = connexion_app.app.config

    # Start the service
    if port is None:
        port = config.get('SERVER_PORT')
    if server is None:
        server = config.get('SERVER')
    monitor_system(10)
    connexion_app.run(port=port, server=server)
