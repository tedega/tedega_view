#!/usr/bin/env python3
import logging
import venusian
import connexion

from lib.swagger import (
    write_config,
    generate_config
)
from api import (
    registry
)

SERVICE_CONFIG = "SERVICE_CONFIG"
"""Name of the environment valirable which stores the path to the custom
service configuration. See
http://flask.pocoo.org/docs/dev/config/#configuring-from-files
"""
SERVICE_MODE = "SERVICE_MODE"
"""Name of the environment valirable which stores mode of the
application. The following modes are available:
1. Development
2. Production
"""


# Create a new logger for this service.
logger = logging.getLogger(__name__)


def start_service(swagger_config, modul, port=None, server=None):
    scanner = venusian.Scanner(registry=registry)
    scanner.scan(modul)

    # Generate the config file
    swagger_config = generate_config(swagger_config, registry)


    connexion_app = connexion.App(__name__)
    config = connexion_app.app.config

    if port is None:
        port = config.get('SERVER_PORT')
    if server is None:
        server = config.get('SERVER')

    # Setup Logging
    if config.get("DEBUG"):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    with write_config(swagger_config) as swagger_config_file:
        connexion_app.add_api(swagger_config_file)
    connexion_app.run(port=port, server=server)
