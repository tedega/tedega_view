#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Modul to generate parts of the swagger API specification based on
attributes of the domain model.
"""
import logging
import datetime
from string import Template as StringTemplate
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from mako.template import Template

logger = logging.getLogger(__name__)

definitions_template_src = """
definitions:
  % for item in data["items"]:
  ${item["name"]}:
    type: ${item["type"]}
    %if len(item["required"]) > 0:
    required:
    % for field in item["required"]:
      - ${field}
    % endfor
    % endif
    properties:
    % for field in item["properties"]:
      ${field["name"]}:
        type: ${field["type"]}
        description: ${field["description"]}
        example: ${field["example"]}
        readOnly: ${field["readonly"]}
    % endfor

  % endfor
"""
definitions_template = Template(definitions_template_src)


def _get_property_type(prop):
    """Inspects the given SQLA column and returns the type defintion for
    the API"""
    ptype = str(prop.type).lower()
    if ptype == "integer":
        return ptype
    elif ptype == "date":
        return "string"
    elif ptype == "datetime":
        return "string"
    elif ptype == "varchar":
        return "string"
    else:
        raise TypeError("Unsupported type of property: {}".format(prop.type))


def _get_property_example(prop):
    """Inspects the given SQLA column and returns a example based on the
    columns datatype for the API"""
    if prop.info.get("example"):
        return prop.info["example"]

    ptype = str(prop.type).lower()
    if ptype == "integer":
        return "123"
    elif ptype == "date":
        return datetime.date.today().isoformat()
    elif ptype == "datetime":
        return datetime.datetime.utcnow().isoformat()
    elif ptype == "varchar":
        return "Yeah! I'm a string"
    else:
        raise TypeError("Unsupported type of property: {}".format(prop.type))


def _get_property_description(prop):
    """Inspects the given SQLA column and return further descriptions
    for the swagger API"""
    return prop.info.get("description", "No description available")


def _get_property_readonly(prop):
    """Inspects the given SQLA column and return if the column is marked
    to be readonly in the API."""
    return str(prop.info.get("readonly", False)).lower()


def _get_property_requied(prop):
    """Inspects the given SQLA column and return if the column is marked
    to be required (not nullable in SQL sense) in the API."""
    return not prop.nullable


def generate_part_definitions(model):
    """Will generate the definitions part of the swagger config based on
    the given model.

    :model: Class of the root of the domain model.
    :returns: String

    """
    def get_properties(model):
        properties = []
        for column in model.__table__.columns:
            c_attr = {}
            c_attr["name"] = column.key
            c_attr["type"] = _get_property_type(column)
            c_attr["description"] = _get_property_description(column)
            c_attr["example"] = _get_property_example(column)
            c_attr["readonly"] = _get_property_readonly(column)
            c_attr["required"] = _get_property_requied(column)
            properties.append(c_attr)
        return properties

    def get_item(model):
        item = {}
        item["name"] = model.__name__
        item["type"] = "object"
        item['properties'] = get_properties(model)
        item['required'] = [p["name"] for p in item["properties"] if p["required"]]
        return item

    definition = {}
    definition['items'] = [get_item(model)]
    return definition


@contextmanager
def write_config(config):
    """Will write the configuraiton into a temporary file and returns
    the path to the file.

    :config: configuratioin as string.
    :returns: Path of the dynamically generated config.
    """
    tmpfile = NamedTemporaryFile()
    tmpfile.write(config)
    tmpfile.flush()
    yield tmpfile.name
    tmpfile.close()


def generate_config(template, model):
    """Will generate a swagger API configuration. The configuration file
    is build on the base of the given template configuration and is
    extended by dynamically generated parts based on the given model.

    :template: Path to the template of the swagger config.
    :model: Class of the root of the domain model.
    :returns: Dynamically generated config as string.
    """
    definitions = definitions_template.render(data=generate_part_definitions(model))
    with open(template) as t:
        content = StringTemplate(t.read())
        content = content.safe_substitute(definitions=definitions)
        logger.debug(content)
    return content
