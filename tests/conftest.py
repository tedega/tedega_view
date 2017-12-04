import os
import pytest
import tedega_view


@pytest.fixture
def app():
    swagger_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "swagger.yaml"))
    tedega_view.server.register_endpoints(tedega_view)
    app = tedega_view.server.create_server(tedega_view, swagger_config)
    return app.app
