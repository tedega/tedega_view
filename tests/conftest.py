import os
import pytest
import tedega_view


@pytest.fixture
def app():
    swagger_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "swagger.yaml"))
    app = tedega_view.service.create_service(swagger_config, tedega_view)
    return app.app
