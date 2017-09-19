#!/usr/bin/env python3
import os
import logging
import connexion
from connexion import NoContent

# Name of the environment valirable which stores the path to the custom
# service configuration. See
# http://flask.pocoo.org/docs/dev/config/#configuring-from-files
SERVICE_CONFIG = "SERVICE_CONFIG"

# Our memory-only item storage
ITEMS = {}

# Create a new logger for this service.
logger = logging.getLogger(__name__)


def get_items(limit):
    return [item for item in ITEMS.values()][:limit]


def get_item(item_id):
    item = ITEMS.get(item_id)
    return item or ('Not found', 404)


def put_item(item_id, item):
    exists = item_id in ITEMS
    if exists:
        logger.info('Updating item %s..', item_id)
        ITEMS[item_id].update(item)
    else:
        logger.info('Creating item %s..', item_id)
        ITEMS[item_id] = item
    return NoContent, (200 if exists else 201)


def delete_item(item_id):
    if item_id in ITEMS:
        logger.info('Deleting item %s..', item_id)
        del ITEMS[item_id]
        return NoContent, 204
    else:
        return NoContent, 404

if __name__ == '__main__':
    connexion_app = connexion.App(__name__)
    app = connexion_app.app

    # Load configuration
    config = app.config
    config.from_object('ringo_service.config.DevelopmentConfig')
    if os.environ.get(SERVICE_CONFIG):
        config.from_envvar(SERVICE_CONFIG)

    # Setup Logging
    if config.get("DEBUG"):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    connexion_app.add_api(config.get('API_CONFIG'))
    connexion_app.run(port=config.get('SERVER_PORT'),
                      server=config.get('SERVER'))
