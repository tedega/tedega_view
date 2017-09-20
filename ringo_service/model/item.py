#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import inspect

Base = declarative_base()


def create_model(engine):
    """Will trigger the creation of all needed tables in the database
    for the model."""
    Base.metadata.create_all(engine)


########################################################################
#             Helper methods to load or create new items.              #
########################################################################

def load_items(db):
    """Loads all items from the database and returns it as a list.

    :db: DB session
    :returns: List of :class:Item
    """
    return db.query(Item).all()


def load_item(db, item_id):
    """Loads a single item from the database and returns it. The item to
    be loaded is identified by its ID. If no item can be loaded (e.g
    does not exist) the function returns None.

    :db: DB session
    :item_id: ID of the item to be loaded.
    :returns: Single :class:Item

    """
    try:
        return db.query(Item).filter(Item.id == item_id).one()
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
    return Item(values)


########################################################################
#       Classes of the models witin the domain of this service.        #
########################################################################

class BaseItem(object):
    """Base for all items in the domain of this service. It provides
    simple helper methods to retreive and set values of a single
    item."""
    __tablename__ = "items"
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
        mapper = inspect(self)
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


class Item(BaseItem, Base):
    """Dummy implementation of a single item within this service."""
    pass
