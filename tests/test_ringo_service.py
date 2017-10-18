#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ringo_service
----------------------------------

Tests for `ringo_service` module.
"""

import pytest


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_get_params_from_path():
    from ringo_service.api import get_params_from_path
    path = "/foo/{item_id}/bar/{baz}"
    params = get_params_from_path(path)
    assert len(params) == 2
    assert params[0] == "item_id"
    assert params[1] == "baz"
