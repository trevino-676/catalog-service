"""
author: ErrataSEV
date: 21/07/2021
"""
from app import mongo, app
from app.model.dto import DTO


class Suppliers(DTO):
    collection = mongo.db[app.config["PROVEEDORES_COLLECTION"]]

    @classmethod
    def find_all(cls, filters: dict):
        try:
            suppliers = cls.collection.find(filters)
            return list(suppliers)
        except Exception as e:
            app.logger.error(e)
            return None

    @classmethod
    def update_one(cls, filters: str, field: dict):
        update = {"$set": field, "$currentDate": {"Fecha_act": True} }
        try:
            supplier = cls.collection.update_one({"_id":filters}, update)
            return supplier
        except Exception as e:
            app.logger.error(e)
            return None
