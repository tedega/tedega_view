#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tedega_service
----------------------------------

Tests for `tedega_service` module.
"""


def test_version(client):
    from tedega_service import __version__
    res = client.get('/test?action=foo')
    assert res.status_code == 204
    res = client.get('/test?action=version')
    assert res.json == u'{"version": "%s"}' % __version__
    res = client.get('/test?action=clienterror')
    assert res.status_code == 400
    res = client.get('/test?action=autherror')
    assert res.status_code == 403
    res = client.get('/test?action=notfound')
    assert res.status_code == 404
    res = client.get('/test?action=genericerror')
    assert res.status_code == 500
