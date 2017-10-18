#!/usr/bin/env python
# -*- coding: utf-8 -*-
import venusian
from swaggenerator import EndpointConfig


def config_service_endpoint(path, method):
    def real_decorator(function):
        def callback(scanner, name, ob):
            scanner.registry.add_endpoint(path, method, function)
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


class Registry(object):
    def __init__(self):
        self.models = []
        self.endpoints = {}

    def add_endpoint(self, path, method, function):
        if "{}:{}".format(path, method) not in self.endpoints:
            config = EndpointConfig(path, method, function)
            self.endpoints[str(config)] = config

    def get_endpoint(self, path, method):
        return self.endpoints.get("{}:{}".format(path, method))

    def add_model(self, name, clazz):
        self.models.append((name, clazz))


registry = Registry()