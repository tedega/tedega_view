#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import venusian
from connexion import NoContent

from model.converters import (
    from_json,
    to_json
)

logger = logging.getLogger(__name__)

########################################################################
#                           Service registry                           #
########################################################################


class Registry(object):
    def __init__(self):
        self.registered = []

    def add(self, name, ob):
        self.registered.append((name, ob))

    def get(self, name):
        for key, func in self.registered:
            if name == key:
                return func
        return None

registry = Registry()

########################################################################
#        Decorators to configure a service in the domain model         #
########################################################################


def service_config(wrapped):
    def callback(scanner, name, ob):
        scanner.registry.add(name, wrapped)
    venusian.attach(wrapped, callback)
    return wrapped

########################################################################
#                            CRUD Endpoints                            #
########################################################################

# def get_items(limit):
#     return [to_json(item.values) for item in load_items(db)][:limit]


def search(limit):
    service = registry.get("search")
    items = service()
    return [to_json(item.get_values()) for item in items][:limit]


def create(item):
    service = registry.get("create")
    try:
        values = from_json(item)
        new_item = service(values["name"], values["password"])
        logger.info('Creating item %s..', new_item.id)
        return NoContent, 201
    except Exception:
        logger.error('Failed creating item ..')
        raise


def read(item_id):
    service = registry.get("read")
    try:
        item = service(item_id)
        return to_json(item.get_values())
    except:
        return NoContent, 404


def update(item_id, item):
    service = registry.get("update")
    try:
        service(item_id, from_json(item))
        logger.info('Updating item %s..', item_id)
        return NoContent, 200
    except Exception:
        logger.error('Failed updating item %s..', item_id)
        raise


def delete(item_id):
    service = registry.get("delete")
    try:
        service(item_id)
        logger.info('Deleting item %s..', item_id)
        return NoContent, 204
    except Exception:
        logger.error('Failed deleting item %s..', item_id)
        raise
