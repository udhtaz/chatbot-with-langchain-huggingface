import os
from dotenv import load_dotenv, find_dotenv
from urllib.parse import quote, quote_plus


_ = load_dotenv(find_dotenv())

load_dotenv()

import logging
logging.basicConfig(level = logging.INFO)


class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ROWS_PER_PAGE = 20
    CORS_HEADERS = 'Content-Type'
    huggingface_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = huggingface_token


class DevConfig(Config):
    """Development config. For venv on local"""
    FLASK_ENV = "development"
    FLASK_DEBUG = True


class TestConfig(Config):
    """Testing config. for docker in local"""
    TESTING = True
    FLASK_DEBUG = True


class ProdConfig(Config):
    """Production config."""
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    ROWS_PER_PAGE = 20


config_classes={"development":DevConfig, "testing": TestConfig,
                "production": ProdConfig}

def load_config():
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    env_config = config_classes[ENVIRONMENT.lower()]
    return env_config

