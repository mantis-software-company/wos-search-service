import logging

from flask import Flask
from flask_smorest import Api
from pyctuator.pyctuator import Pyctuator

from .modules.rest.views import rest_blueprint
from .utils.settings import apply_settings

app = Flask(__name__)

logging.basicConfig(level=logging.ERROR)
log = logging.getLogger(__name__)

apply_settings(app)
actuator = Pyctuator(
    app,
    app_name=app.config.get('ACTUATOR_SERVICE_NAME'),
    app_description=app.config.get('API_TITLE'),
    app_url=f"http://{app.config['SERVER_NAME']}/",
    pyctuator_endpoint_url=app.config.get("ACTUATOR_BASE_URI"),
    registration_url=None
)
actuator.set_build_info(
    name=app.config.get('ACTUATOR_SERVICE_NAME'),
    version=app.config.get("API_VERSION"),
)

api = Api(app)
Api.DEFAULT_ERROR_RESPONSE_NAME = None
api.register_blueprint(rest_blueprint)


if __name__ == "__main__":
    app.run()