"""
author: Luis Manuel Torres Trevino
description: Este archivo crea toda la aplicacion de flask
"""
import os

from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt import JWT

app = Flask(__name__)
app.config.from_object("config.Config")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

mongo = PyMongo(app, authSource="admin")

from app.service import authenticate, identity

jwt = JWT(app, authenticate, identity)

from app.routes import user_routes

app.register_blueprint(user_routes)

from app.routes import company_routes

app.register_blueprint(company_routes)

from app.routes import supplier_routes

app.register_blueprint(supplier_routes)
