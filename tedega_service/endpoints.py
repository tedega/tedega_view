#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import re
import connexion
import voorhees
from connexion import NoContent
from connexion.resolver import Resolver

from .registry import registry, config_service_endpoint
from .exceptions import NotFound, ClientError, AuthError


@config_service_endpoint(path="/test", method="GET")
def test(action):
    from ringo_service import __version__
    from ringo_service import ClientError, AuthError, NotFound
    if action == "version":
        return {'version': __version__}
    if action == "clienterror":
        raise ClientError
    if action == "autherror":
        raise AuthError
    if action == "notfound":
        raise NotFound
    if action == "genericerror":
        raise Exception("I failed!")
    else:
        return None


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
        return self.function_resolver(operation_id)

        # Because we currently always return the endpoint_proxy the
        # import can not fail. For this reason I commented out this code
        # but leave it here in case I probably want to enhance the
        # functionallity of the resolver.
        # try:
        #     return self.function_resolver(operation_id)
        # except ImportError as e:
        #     msg = ('Cannot resolve operationId "{}"! '
        #            'Import error was "{}"').format(operation_id, str(e))
        #     raise ResolverError(msg, sys.exc_info())
        # except (AttributeError, ValueError) as e:
        #     raise ResolverError(str(e), sys.exc_info())


def endpoint_proxy(*args, **kwargs):
    """Proxy for all configured service endpoints.

    The method will forward the request to the configured service in the
    registry.

    :args: Currently ignored
    :kwargs: Dictionary with function arguments preparsed as defined by
    the swagger config.
    :returns: Response sent to the client.
    """
    # Get the configured service from the registry.
    path = _get_request_path()
    method = _get_request_method()
    endpoint = registry.get_endpoint(path, method)
    service = endpoint.function

    # Build params for the service
    params = _get_service_parameters(service, kwargs)

    try:
        # Call the service TODO: Do we need to handle more return codes
        # like 201? What is a good way to distiguish between 200 and 201
        # based on the return value? (ti) <2017-10-07 09:55>
        result = service(**params)

        # Result. Return it with status code 200
        if result:
            return voorhees.to_json(result), 200
        # No Result. Return it with status code 204
        else:
            return NoContent, 204
    except ClientError as e:
        # Client request was wrong.
        return e.message, 400
    except NotFound:
        # Item could not befound. Return 404
        return NoContent, 404
    except AuthError as e:
        # User can not be authorized or authenticated.
        return voorhees.to_json(e.message), 403
    except Exception:
        # General Error. Will result in a 500
        raise


def _get_request_path():
    """Will return the path of the current request."""
    request = connexion.request
    url_rule = request.url_rule
    # `url_rule` comes from request.url_rule and has a different
    # notation than the path definitions in the swagger config. To be
    # able to find the appropriate function to call in a request we need
    # to transform the url_rule into the form swagger uses.

    # Remove type information e.g. <int:foo> -> <foo>
    url_rule = re.sub("<.+:", "<", str(url_rule))
    return url_rule.replace("<", "{").replace(">", "}")


def _get_request_method():
    """Will return the method (GET, POST...) of the current request."""
    request = connexion.request
    return request.method


def _get_service_parameters(service, parameters):
    """Will return parameters suitable to call the given service.

    Example::

        {'values': '{"password": "Password", "id": 1, "name": "User1"}'}

    :service: Service callable.
    :parameters: Dictionary with function arguments preparsed as defined
                 by the swagger config.
    :returns: Dictionary of service parameters.
    """

    def looks_like_json(value):
        if (value.startswith("{") or value.startswith("[")):
            return True
        return False

    # First check which parameters are wanted by the given service.
    service_wants = inspect.getargspec(service)[0]
    service_send = {}

    # Iterate over all function arguments and check if any of those
    # arguments matches on of the argumentsthe service wants.
    for param in parameters:
        value = parameters[param]
        if isinstance(value, bytes):
            value = value.decode("utf-8")
            if looks_like_json(value):
                value = voorhees.from_json(value)
        if param in service_wants:
            service_send[param] = value
        elif isinstance(value, dict):
            for subparam in value:
                if subparam in service_wants:
                    service_send[subparam] = value[subparam]
    return service_send