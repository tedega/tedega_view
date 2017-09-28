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

    def add_api(self, name, function):
        self.apis.append((name, function))

    def add_model(self, name, clazz):
        self.models.append((name, clazz))

    def get_api(self, name):
        for key, func in self.registered:
            if name == key:
                return func
        return None

registry = Registry()

########################################################################
#        Decorators to configure a service in the domain model         #
########################################################################


def register_api(path=None, method="GET", endpoint=None):
    def real_decorator(function):
        def callback(scanner, name, ob):
            scanner.registry.add_api(name, function)
        venusian.attach(function, callback)
        return function
    return real_decorator


def register_model():
    def real_decorator(clazz):
        def callback(scanner, name, ob):
            scanner.registry.add_model(name, clazz)
        venusian.attach(clazz, callback)
        return clazz
    return real_decorator

########################################################################
#                            CRUD Endpoints                            #
########################################################################


def search(limit):
    service = registry.get_api("search")
    items = service()
    return [voorhees.to_json(item.get_values()) for item in items][:limit]


def create(item):
    service = registry.get_api("create")
    try:
        values = voorhees.from_json(item)
        new_item = service(values["name"], values["password"])
        logger.info('Creating item %s..', new_item.id)
        return NoContent, 201
    except Exception:
        logger.error('Failed creating item ..')
        raise


def read(item_id):
    service = registry.get_api("read")
    try:
        item = service(item_id)
        return to_json(item.get_values())
    except:
        return NoContent, 404


def update(item_id, item):
    service = registry.get_api("update")
    try:
        service(item_id, voorhees.from_json(item))
        logger.info('Updating item %s..', item_id)
        return NoContent, 200
    except Exception:
        logger.error('Failed updating item %s..', item_id)
        raise


def delete(item_id):
    service = registry.get_api("delete")
    try:
        service(item_id)
        logger.info('Deleting item %s..', item_id)
        return NoContent, 204
    except Exception:
        logger.error('Failed deleting item %s..', item_id)
        raise
