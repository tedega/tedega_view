#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example domain."""
import sqlalchemy as sa


class Foo(object):
    __tablename__ = "foo"
    name = sa.Column("name", sa.String, info={"description": "Name of the Item."})
    date = sa.Column("date", sa.Date, info={"description": "A simple datefield."})


class Bar(object):
    __tablename__ = "bar"
    name = sa.Column("name", sa.String)
