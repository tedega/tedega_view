===============================
Ringo Service
===============================


.. image:: https://img.shields.io/pypi/v/ringo_service.svg
        :target: https://pypi.python.org/pypi/ringo_service

.. image:: https://img.shields.io/travis/toirl/ringo_service.svg
        :target: https://travis-ci.org/toirl/ringo_service

.. image:: https://readthedocs.org/projects/ringo-service/badge/?version=latest
        :target: https://ringo-service.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/toirl/ringo_service/shield.svg
     :target: https://pyup.io/repos/github/toirl/ringo_service/
     :alt: Updates


Ringo service is a framework to build microservices. It can be used to make a
specic domain model available through a REST API.

Ringo service use `connexion <https://github.com/zalando/connexion>`_ to
generate the endpoints of the service based on a `swagger
<https://swagger.io>`_ specification. The specification is partially
dynamically generated based on the attributes of the domain model.

* Free software: MIT license
* Documentation: https://ringo-service.readthedocs.io.


Features
--------

* Pluggable domain model.
* REST API with automatic generated CRUD endpoints.
* RDBMS agnostic
* Runs with Python version 2.7.x and >= 3.5

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

