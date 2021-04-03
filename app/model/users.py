"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase para el modelo de usuarios
"""
from app import mongo, app
from app.model import DTO


class User(DTO):
    
    collection = mongo.db[app.config["DB_NAME"]]