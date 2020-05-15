#!/usr/bin/env python3
import os
import re
import importlib
import venusian
from flask_cors import CORS
import connexion

from .registry import registry
from .views import ViewResolver


def register_endpoints(modul):
    # Scan for service endpoints and models in the given modul and store
    # these in the registry.
    scanner = venusian.Scanner(registry=registry)
    scanner.scan(modul, ignore=[re.compile('wsgi$').search])


def create_application(modulname, swagger_file="swagger.yaml", run_on_init=None):
    """Will create a connexion application for the given domain modul in
    `modulname`. The method will register all endpoints of the modul and
    make them available with the definden REST-API given in the
    `swagger_file`.

    The funtion can optionally run a list of functions when the
    application is created. This can be used to start background
    processes like monitoring. The callable are give as a list of
    tuples. The first element in the tuple is the callable and the
    second element are the arguments used to call the callable.

    :modulname: String of the name of the domain modul/package.
    :swagger_file: Name of the Swagger config relativ to the given modul/package.
    :run_on_init: List of callable which are called after the application has been created.
    :returns: Connexion application.

    """
    modul = importlib.import_module(modulname)
    register_endpoints(modul)
    package_directory = os.path.dirname(os.path.abspath(modul.__file__))
    swagger = os.path.abspath(os.path.join(package_directory, swagger_file))
    connexion_app = connexion.App(__name__)
    connexion_app.add_api(swagger, resolver=ViewResolver())
    CORS(connexion_app.app)

    if isinstance(run_on_init, list):
        for func, func_args in run_on_init:
            if func_args:
                if len(func_args) == 2:
                    if func_args[0]:
                        func(func_args[0], **func_args[1])
                    else:
                        func(**func_args[1])
                else:
                    func(func_args)
            else:
                func()

    return connexion_app
