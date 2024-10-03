import io
from flask import Flask
from flask_cors import CORS
from app.config import load_config
from app.utils import get_gem_pdf, get_worldbank_data

import logging
logging.basicConfig(level = logging.INFO)

def create_app():
    app = Flask(__name__)
    config_class = load_config()
    app.config.from_object(config_class)

    CORS(app, supports_credentials=True)

    from app.api import api_bp
    app.register_blueprint(api_bp)

    # Fetch World Bank data and download GEM PDF on app startup
    with app.app_context():
        logging.info("Fetching World Bank data...")
        get_worldbank_data()
        
        logging.info("Downloading GEM PDF...")
        pdf_url = "https://gemconsortium.org/file/open?fileId=51377"
        get_gem_pdf(pdf_url)

    return app
