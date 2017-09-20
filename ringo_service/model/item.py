#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import importlib
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()
Base.metadata.extend_existing = True

DOMAIN = None
"""Root class of the domain model for this service. The service will
return items of this class when querying the service."""


def create_model(engine, domain):
    """Will trigger the creation of all needed tables in the database
    for the model."""
    global DOMAIN

    # Split the configured import path to the domain model to get the
    # root of the domain model and the complete model.
    import_path = domain.split(".")
    modul_path = ".".join(import_path[0:-1])
    domain_root = import_path[-1]

    # Now import the complete modul and iterate over the classes of the
    # domain. In case the class is intended to be table in the database
    # we will dynamically craft the class for this. If the class is the
    # configured root of the domain. Save it as DOMAIN.
    MODUL = importlib.import_module(modul_path)
    for k, v in MODUL.__dict__.items():
        if inspect.isclass(v) and hasattr(v, "__tablename__"):
            clazz = craft_class(v, v.__name__)
            if clazz.__name__ == domain_root:
                DOMAIN = clazz

    # After we imported all relevant classes we can create the tables in
    # the database.
    Base.metadata.create_all(engine)


def craft_class(Class, name):
    """Will dynamically craft a new Class based on the given Class with
    the given name. The resulting class will inherit from multiple base
    classes which makes the crafted class compatible with the
    service."""
    return type(name, (Class, BaseItem, Base, ), dict())


########################################################################
#             Helper methods to load or create new items.              #
########################################################################

def load_items(db):
    """Loads all items from the database and returns it as a list.

    :db: DB session
    :returns: List of :class:Item
    """
    return db.query(DOMAIN).all()


def load_item(db, item_id):
    """Loads a single item from the database and returns it. The item to
    be loaded is identified by its ID. If no item can be loaded (e.g
    does not exist) the function returns None.

    :db: DB session
    :item_id: ID of the item to be loaded.
    :returns: Single :class:Item

    """
    try:
        return db.query(DOMAIN).filter(DOMAIN.id == item_id).one()
    except NoResultFound:
        return None


def create_item(values):
    """Creates a new item and returns it. The new item will be
    initialized with the given values.

    Please not the the values **must** include a valid value for the ID
    of the item.

    :values: Dictionary of values for the new item.
    :returns: a Single :class:Item

    """
    return DOMAIN(values)


########################################################################
#       Classes of the models witin the domain of this service.        #
########################################################################

class BaseItem(object):
    """Base for all items in the domain of this service. It provides
    simple helper methods to retreive and set values of a single
    item."""
    id = sa.Column(sa.Integer, primary_key=True)
    created = sa.Column(sa.DateTime)
    updated = sa.Column(sa.DateTime)

    def __init__(self, values):
        if "id" in values and values["id"]:
            self.id = values["id"]
            self.set_values(values)
            self.created = datetime.utcnow()
            self.updated = datetime.utcnow()
        else:
            raise ValueError("Values must include at least a value for the ID of the item.")

    @property
    def fields(self):
        """Returns the names of all columns of the item.

        :returns: List of fieldnames
        """
        mapper = sa.inspect(self)
        return [column.key for column in mapper.attrs]

    @property
    def values(self):
        """Returns the values of the item as a dictionary.

        :returns: Dictionary of values of the item.
        """
        values = {}
        for field in self.fields:
            values[field] = getattr(self, field)
        return values

    def set_values(self, values):
        """Will set values of the item based on the given dictionary.

        :values: Dictionary of values.
        """
        for field in self.fields:
            value = values.get(field)
            if value is not None:
                setattr(self, field, value)
