===============================
Tedega Service
===============================


.. image:: https://img.shields.io/pypi/v/tedega_service.svg
        :target: https://pypi.python.org/pypi/tedega_service

.. image:: https://img.shields.io/travis/toirl/tedega_service.svg
        :target: https://travis-ci.org/toirl/tedega_service

.. image:: https://readthedocs.org/projects/tedega-service/badge/?version=latest
        :target: https://tedega-service.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/toirl/tedega_service/shield.svg
     :target: https://pyup.io/repos/github/toirl/tedega_service/
     :alt: Updates


Tedega service is a framework to build microservices. It can be used to make a
specic domain model available through a REST API.

Tedega service use `connexion <https://github.com/zalando/connexion>`_ to
generate the endpoints of the service based on a `swagger
<https://swagger.io>`_ specification. The specification is partially
dynamically generated based on the attributes of the domain model.

* Free software: MIT license
* Documentation: https://tedega-service.readthedocs.io.


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

