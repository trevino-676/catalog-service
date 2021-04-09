"""
author: Luis Manuel Torres Trevino
description: Este archivo crea toda la aplicacion de flask
"""
import os

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object("config.Config")

mongo = PyMongo(app)

from app.routes import user_routes

app.register_blueprint(user_routes)