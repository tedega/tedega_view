=====
Usage
=====

Configure a service endpoint
----------------------------

.. autofunction:: tedega_view.api.config_service_endpoint


Configure a service model
-------------------------

.. autofunction:: tedega_view.api.config_service_model

Start the service
-----------------

.. autofunction:: tedega_view.service.start_service

==========================
Predefined services (CRUD)
==========================

.. autofunction:: tedega_view.api.search
.. autofunction:: tedega_view.api.create
.. autofunction:: tedega_view.api.read
.. autofunction:: tedega_view.api.update
.. autofunction:: tedega_view.api.delete


.. Setup Domain model
.. ------------------
..
.. .. literalinclude:: ../tedega_view/model/example.py
..    :language: python
..    :emphasize-lines: 12,15-18
..    :linenos:
..
.. Configure service
.. -----------------
.. The service is configured by setting enviroment variables. The variable
.. are used to configure mode of the service and to customize the settings.
..
.. The mode will configure the service with some usefull default. E.g in
.. development mode the debug output is enablder.
..
.. To customize the settings you can define the path to a config file. This
.. file include specific configuration options which will  overwrite the
.. default settings.
..
.. .. important::
..
..     You will need to configure at least the DOMAIN_MODUL. Without
..     configured DOMAIN_MODUL the server will not start.
..
.. .. rubric:: SERVICE_MODE
..
.. 1. Development (default)
.. 2. Production
..
.. .. rubric:: SERVICE_CONIG
..
.. Start service
.. -------------
..
.. Example::
..
..     $ export SERVICE_MODE=Production
..     $ export SERVICE_CONFIG=myconfig.cfg
..     $ python tedega_view/service.py
