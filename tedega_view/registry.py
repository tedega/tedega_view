#!/usr/bin/env python
# -*- coding: utf-8 -*-
import venusian


class ServiceConfig(object):

    """Class to store the configuration of a Endpoint."""

    def __init__(self, path, method, auth, function):
        """TODO: to be defined1."""
        self.path = path
        self.method = method
        self.auth = auth
        self.function = function

    def __str__(self):
        return "{}:{}".format(self.path, self.method)


def config_service_endpoint(path, method, auth):
    def real_decorator(function):
        def callback(scanner, name, ob):
            scanner.registry.add_endpoint(path, method, auth, function)
        venusian.attach(function, callback)
        return function
    return real_decorator


class Registry(object):
    def __init__(self):
        self.endpoints = {}

    def add_endpoint(self, path, method, auth, function):
        if "{}:{}".format(path, method) not in self.endpoints:
            config = ServiceConfig(path, method, auth, function)
            self.endpoints[str(config)] = config

    def get_endpoint(self, path, method):
        return self.endpoints.get("{}:{}".format(path, method))


registry = Registry()
