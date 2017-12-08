#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import re
import connexion
import voorhees
from connexion import NoContent
from connexion.resolver import Resolver

from tedega_share import get_logger, log_proctime

from .registry import registry, config_view_endpoint
from .exceptions import NotFound, ClientError, AuthError


def log_returncode(func):

    def wrap(*args, **kwargs):
        log = get_logger()
        result, code = func(*args, **kwargs)
        if code > 299:
            log.error({"code": code}, "RETURNCODE")
        else:
            log.info({"code": code}, "RETURNCODE")
        return result, code
    return wrap


def log_request(func):

    def wrap(*args, **kwargs):
        request = connexion.request
        path = _get_request_path()
        method = _get_request_method()
        log = get_logger()
        log.info({"path": path, "method": method, "form": request.form, "args": request.args}, "REQUEST")
        result, code = func(*args, **kwargs)
        return result, code
    return wrap


def log_auth(func):

    def wrap(*args, **kwargs):
        log = get_logger()
        log.info("Test", "AUTH")
        result, code = func(*args, **kwargs)
        return result, code
    return wrap


@config_view_endpoint(path="/test", method="GET", auth=None)
def test(action):
    from tedega_view import __version__
    from tedega_view import ClientError, AuthError, NotFound
    if action == "version":
        return {'version': __version__}
    if action == "clienterror":
        raise ClientError("Test ClientError")
    if action == "autherror":
        raise AuthError("Test AuthError")
    if action == "notfound":
        raise NotFound
    if action == "genericerror":
        raise Exception("I failed!")
    else:
        return None


class ViewResolver(Resolver):
    """Specific Resolver to map a request to a service endpoint. Usually
    the default resolver of connexion will take the operationID of the
    swagger config to determine the correct endpoint. But in
    contrast we want to map **all** requests to a single endpoint which
    will act like a proxy."""

    def __init__(self):
        self.function_resolver = lambda x: proxy

    def resolve_function_from_operation_id(self, operation_id):
        """
        Invokes the function_resolver
        :type operation_id: str
        """
        return self.function_resolver(operation_id)

        # Because we currently always return the proxy the
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


def authorize(checker):
    """Will authorize the incoming request. If the request is authorized
    the method return True, other wise False.

    To authorize the current request a JWT is extracted from the header
    of the request.

    The function will do general checks on the validity of the JWT. If
    those test are successful the JWT is than provided to a authorize
    checker which implements more specific checks. The handler is
    defined in the Domain model and was provided when registering the
    view.
    :checker: Authorize handler
    :returns: True or False

    """
    jwt = _get_request_jwt()
    if jwt is None:
        raise AuthError("Can not extract JWT token from header")

    # Do generic checks
    # TODO: Check if JWT is expired. (ti) <2017-11-29 09:58>

    # Do specific checks. The specific checker either returns unspecific
    # True or False or raises a AuthError with a more informations in
    # the Exception.
    result = checker(jwt)
    if result is True:
        return True
    else:
        raise AuthError("Authorization failed for unknown reason")


@log_request
@log_returncode
@log_proctime
def proxy(*args, **kwargs):
    """Proxy for all configured service endpoints.

    The method will forward the request to the configured service in the
    registry.

    :args: Currently ignored
    :kwargs: Dictionary with function arguments preparsed as defined by
    the swagger config.
    :returns: Response sent to the client.
    """
    log = get_logger()
    try:
        # Get the configured service from the registry.
        path = _get_request_path()
        method = _get_request_method()

        endpoint = registry.get_endpoint(path, method)
        if endpoint is None:
            raise NotFound("Can not find mapped function for request")

        # Authorize the request if the endpoint is configured to need
        # authorization.
        if endpoint.auth:
            authorize(endpoint.auth)

        # Build params for the service
        service = endpoint.function
        params = _get_endpoint_parameter(service, kwargs)

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
        log.error(e.message)
        return e.message, 400
    except NotFound:
        # Item could not befound. Return 404
        return NoContent, 404
    except AuthError as e:
        # User can not be authorized or authenticated.
        log.error(e.message)
        return voorhees.to_json(e.message), 403
    except Exception as e:
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


def _get_request_jwt():
    """Will return the encoded JWT Token from the header if available.
    Else None"""
    # request = connexion.request
    return None


def _get_endpoint_parameter(endpoint, parameters):
    """Will return parameters suitable to call the given endpoint.

    Example::

        {'values': '{"password": "Password", "id": 1, "name": "User1"}'}

    :endpoint: Endpoint callable.
    :parameters: Dictionary with function arguments preparsed as defined
                 by the swagger config.
    :returns: Dictionary of endpoint parameters.
    """

    def looks_like_json(value):
        if (value.startswith("{") or value.startswith("[")):
            return True
        return False

    # First check which parameters are wanted by the given endpoint.
    endpoint_wants = inspect.getargspec(endpoint)[0]
    endpoint_send = {}

    # Iterate over all function arguments and check if any of those
    # arguments matches on of the argumentsthe endpoint wants.
    for param in parameters:
        value = parameters[param]
        if isinstance(value, bytes):
            value = value.decode("utf-8")
            if looks_like_json(value):
                value = voorhees.from_json(value)
        if param in endpoint_wants:
            endpoint_send[param] = value
        elif isinstance(value, dict):
            for subparam in value:
                if subparam in endpoint_wants:
                    endpoint_send[subparam] = value[subparam]
    return endpoint_send
