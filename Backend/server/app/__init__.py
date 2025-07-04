from flask import Flask
from flask_cors import CORS
from server.app.routes.antipyttern import antipyttern_bp
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("flask_app.log", mode='a')
        ]
    )

def create_app():
    app = Flask(__name__)
    CORS(app)
    setup_logging()

    app.register_blueprint(antipyttern_bp, url_prefix='/antipyttern')

    return app
