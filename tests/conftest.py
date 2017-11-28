import os
import pytest
import tedega_service


@pytest.fixture
def app():
    swagger_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "swagger.yaml"))
    app = tedega_service.service.create_service(swagger_config, tedega_service)
    return app.app
