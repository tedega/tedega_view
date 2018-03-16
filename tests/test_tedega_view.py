#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tedega_view
----------------------------------

Tests for `tedega_view` module.
"""
import pytest


def test_version(client):
    from tedega_view import __version__
    res = client.get('/test?action=foo')
    assert res.status_code == 204
    res = client.get('/test?action=version')
    expect = bytes('{\n  "version": "%s"\n}\n' % __version__, "utf8")
    assert res.data == expect
    res = client.get('/test?action=clienterror')
    assert res.status_code == 400
    res = client.get('/test?action=autherror')
    assert res.status_code == 403
    res = client.get('/test?action=notfound')
    assert res.status_code == 404
    res = client.get('/test?action=genericerror')
    assert res.status_code == 500


def test_get_endpoint():

    def xxx(action):
        pass

    from tedega_view.views import _get_endpoint_parameter

    # There is a value for the action parameter
    result = _get_endpoint_parameter(xxx, {"action": "version"})
    assert result == {'action': 'version'}

    # There is a value for the action parameter as encoded JSON.
    with pytest.raises(ValueError):
        result = _get_endpoint_parameter(xxx, bytes("{\"action\": \"version\"}", "utf-8"))

    # There is a no value for the action parameter
    result = _get_endpoint_parameter(xxx, {"notpresent": "version"})
    assert result == {}

    # There is a value for the action parameter with in the nested
    # structure.
    result = _get_endpoint_parameter(xxx, {"values": {"action": "version"}})
    assert result == {'action': 'version'}

    # There is a not value for the action parameter with in the nested
    # structure.
    result = _get_endpoint_parameter(xxx, {"values": {"notpresent": "version"}})
    assert result == {}

    # There is a value for the action parameter with in the nested
    # structure endcoded as JSON.
    result = _get_endpoint_parameter(xxx, {"values": bytes("{\"action\": \"version\"}", "utf-8")})
    assert result == {'action': 'version'}

    # There is no value for the action parameter
    result = _get_endpoint_parameter(xxx, {"values": bytes("foobar", "utf-8")})
    assert result == {}
