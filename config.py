"""
author: Luis Manuel Torres Trevino
descripcion: Este archivo contiene la configuracion para la aplicacion
    del microservicios de usuarios
"""
from os import path, environ

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
DOTENV_PATH = path.join(BASE_DIR, ".env")
load_dotenv(DOTENV_PATH)


class Config:
    """Set flask configuration from .env file"""

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    DEBUG = environ.get("FLASK_DEBUG")

    # Mongo database config
    MONGO_URI = environ.get("MONGO_URI")
    DB_NAME = environ.get("DB_NAME")
