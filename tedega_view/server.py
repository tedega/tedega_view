#!/usr/bin/env python3
import logging
import venusian
from flask_cors import CORS
import connexion

from .registry import registry
from .endpoints import ViewResolver

# Create a new logger for this service.
logger = logging.getLogger(__name__)


def create_server(swagger_config, modul):
    # Scan for service endpoints and models in the given modul and store
    # these in the registry.
    scanner = venusian.Scanner(registry=registry)
    scanner.scan(modul)

    connexion_app = connexion.App(__name__)
    connexion_app.add_api(swagger_config, resolver=ViewResolver())
    CORS(connexion_app.app)
    return connexion_app


def start_server(swagger_config, modul, port=None, server=None):
    connexion_app = create_server(swagger_config, modul)
    config = connexion_app.app.config

    # Setup Logging
    if config.get("DEBUG"):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Start the service
    if port is None:
        port = config.get('SERVER_PORT')
    if server is None:
        server = config.get('SERVER')
    connexion_app.run(port=port, server=server)
