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
        update = {"$set": field, "$currentDate": {"Fecha_act": True}}
        try:
            supplier = cls.collection.update_one({"_id": filters}, update)
            return supplier
        except Exception as e:
            app.logger.error(e)
            return None

    @classmethod
    def get_suppliers_by_company(cls, rfc: str, filters: dict):
        from app.model.company import Company

        company = Company()
        company.find({"rfc": rfc})
        filters["_id"] = {"$in": company.suppliers}

        if "from_date" in filters and "to_date" in filters:
            filters["Fecha_act"] = {
                "$gte": filters["from_date"],
                "$lte": filters["to_date"],
            }
            filters.pop("from_date")
            filters.pop("to_date")

        data = cls.collection.find(filters)
        return list(data)
