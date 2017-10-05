#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import venusian
import voorhees
from connexion import NoContent

logger = logging.getLogger(__name__)

########################################################################
#                           Service registry                           #
########################################################################


class Registry(object):
    def __init__(self):
        self.apis = []
        self.models = []

    def add_endpoint(self, name, function):
        self.apis.append((name, function))

    def add_model(self, name, clazz):
        self.models.append((name, clazz))

    def get_endpoint(self, name):
        for key, func in self.apis:
            if name == key:
                return func
        return None

registry = Registry()

########################################################################
#        Decorators to configure a service in the domain model         #
########################################################################


def config_service_endpoint(path=None, method="GET", endpoint=None):
    def real_decorator(function):
        def callback(scanner, name, ob):
            scanner.registry.add_endpoint(name, function)
        venusian.attach(function, callback)
        return function
    return real_decorator


def config_service_model():
    def real_decorator(clazz):
        def callback(scanner, name, ob):
            scanner.registry.add_model(name, clazz)
        venusian.attach(clazz, callback)
        return clazz
    return real_decorator

########################################################################
#                            CRUD Endpoints                            #
########################################################################


class NotFound(Exception):
    pass


def search(limit):
    service = registry.get_endpoint("search")
    items = service()
    result = []
    for item in items[:limit]:
        result.append(item.get_values())
    return voorhees.to_json(result), 200


def create(values):
    service = registry.get_endpoint("create")
    try:
        values = voorhees.from_json(values)
        new_item = service(values["name"], values["password"])
        logger.info('Creating item %s..', new_item.id)
        return NoContent, 201
    except Exception:
        logger.error('Failed creating item ..')
        raise


def read(item_id):
    service = registry.get_endpoint("read")
    try:
        item = service(item_id)
        return voorhees.to_json(item.get_values())
    except NotFound:
        return NoContent, 404
    except Exception:
        logger.error('Failed reading item %s..', item_id)
        raise


def update(item_id, values):
    service = registry.get_endpoint("update")
    try:
        item = service(item_id, voorhees.from_json(values))
        logger.info('Updating item %s..', item_id)
        return voorhees.to_json(item.get_values()), 200
    except NotFound:
        return NoContent, 404
    except Exception:
        logger.error('Failed updating item %s..', item_id)
        raise


def delete(item_id):
    service = registry.get_endpoint("delete")
    try:
        service(item_id)
        logger.info('Deleting item %s..', item_id)
        return NoContent, 204
    except NotFound:
        return NoContent, 404
    except Exception:
        logger.error('Failed deleting item %s..', item_id)
        raise
