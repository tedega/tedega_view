#!/usr/bin/env python
# -*- coding: utf-8 -*-


class NotFound(Exception):
    pass


class ClientError(Exception):
    def __init__(self, message):
        self.message = message


class AuthError(Exception):
    def __init__(self, message):
        self.message = message
