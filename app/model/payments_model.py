"""
author: ErrataSEV
date: 18/08/2021
"""
from app import mongo, app
from app.model.dto import DTO


class Payments(DTO):
    collection = mongo.db[app.config["PAYMENTS_COMP_COLLECTION"]]

    @classmethod
    def find_all(cls, filters: dict):
        try:
            payments_comp = cls.collection.find(filters)
            return list(payments_comp)
        except Exception as e:
            app.logger.error(e)
            return None

    @classmethod
    def find_agg(cls, filter: list):
        try:
            cfdis = cls.collection.aggregate(filter)
            return list(cfdis)
        except Exception as e:
            app.logger.error(e)
            return None
