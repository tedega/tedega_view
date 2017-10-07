#!/usr/bin/env python3
import sys
import logging
import venusian
import connexion
from connexion.resolver import Resolver
from connexion.exceptions import ResolverError

from lib.swagger import (
    write_config,
    generate_config
)
from api import (
    registry, endpoint_proxy
)

# Create a new logger for this service.
logger = logging.getLogger(__name__)


class ServiceResolver(Resolver):
    """Specific Resolver to map a request to a service endpoint. Usually
    the default resolver of connexion will take the operationID of the
    swagger config to determine the correct endpoint. But in
    contrast we want to map **all** requests to a single endpoint which
    will act like a proxy."""

    def __init__(self):
        self.function_resolver = lambda x: endpoint_proxy

    def resolve_function_from_operation_id(self, operation_id):
        """
        Invokes the function_resolver
        :type operation_id: str
        """
        try:
            return self.function_resolver(operation_id)
        except ImportError as e:
            msg = 'Cannot resolve operationId "{}"! Import error was "{}"'.format(operation_id, str(e))
            raise ResolverError(msg, sys.exc_info())
        except (AttributeError, ValueError) as e:
            raise ResolverError(str(e), sys.exc_info())


def start_service(swagger_config, modul, port=None, server=None):

    # Scan for service endpoints and models in the given modul and store
    # these in the registry.
    scanner = venusian.Scanner(registry=registry)
    scanner.scan(modul)

    connexion_app = connexion.App(__name__)
    config = connexion_app.app.config

    # Setup Logging
    if config.get("DEBUG"):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Generate the config file and it to the app.
    swagger_config = generate_config(swagger_config, registry)
    with write_config(swagger_config) as swagger_config_file:
        connexion_app.add_api(swagger_config_file, resolver=ServiceResolver())

    # Start the service
    if port is None:
        port = config.get('SERVER_PORT')
    if server is None:
        server = config.get('SERVER')
    connexion_app.run(port=port, server=server)
