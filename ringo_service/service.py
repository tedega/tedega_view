#!/usr/bin/env python3
import connexion
import logging

from connexion import NoContent

# our memory-only item storage
ITEMS = {}


def get_items(limit):
    return [item for item in ITEMS.values()][:limit]


def get_item(item_id):
    item = ITEMS.get(item_id)
    return item or ('Not found', 404)


def put_item(item_id, item):
    exists = item_id in ITEMS
    if exists:
        logging.info('Updating item %s..', item_id)
        ITEMS[item_id].update(item)
    else:
        logging.info('Creating item %s..', item_id)
        ITEMS[item_id] = item
    return NoContent, (200 if exists else 201)


def delete_item(item_id):
    if item_id in ITEMS:
        logging.info('Deleting item %s..', item_id)
        del ITEMS[item_id]
        return NoContent, 204
    else:
        return NoContent, 404


logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('../swagger/api.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(port=8080, server='gevent')
