from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

from src.interface.api.routes import bp_orders
from src.interface.api.containers import Container

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.container = Container()

    swagger_config = {
        "headers": [
        ],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": f"/index.html/",
        "title": "Trading API",
    }

    # Initialize Swagger
    swagger = Swagger(app, config=swagger_config)

    @app.route("/healthcheck", methods=["GET"])
    def health_check():
        """
        Healthcheck endpoint
        ---
        tags:
            - Healthcheck
        responses:
            200:
                desecription: Status OK
        """
        return {"message": "Status OK"}, 200

    app.register_blueprint(bp_orders, url_prefix="/api/v1")

    return app
