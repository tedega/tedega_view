#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connection(uri):
    return get_session(uri)


def get_session(uri):
    engine = get_engine(uri)
    Session = sessionmaker(bind=engine)
    return Session()


def get_engine(uri):
    return create_engine(uri, echo=True)
