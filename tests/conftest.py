import os
import pytest
import tedega_view
import tedega_share


@pytest.fixture
def app():
    swagger_config = os.path.abspath(os.path.join(os.path.dirname(__file__), "swagger.yaml"))
    tedega_view.server.register_endpoints(tedega_view)
    run_on_init = [(tedega_share.init_logger, "tedega_view")]
    app = tedega_view.server.create_application("tedega_view", swagger_config, run_on_init=run_on_init)
    return app.app
