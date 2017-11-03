import os
import pytest
import ringo_service


@pytest.fixture
def app():
    swagger_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "swagger.yaml"))
    app = ringo_service.service.create_service(swagger_config, ringo_service)
    return app.app
