"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase para el modelo de usuarios
"""
from app import mongo, app
from app.model import DTO


class User(DTO):

    collection_name = app.config["DB_NAME"]
    collection = mongo.db[collection_name]

    @classmethod
    def get_all_users(cls, filters: dict) -> list:
        """get_all_users
        Ejecuta la funcion __find_all

        Args:
            filters (dict): Filtros para los usuarios

        Returns:
            list: Todos los usuarios que se encontraron
        """
        return cls.__find_all(filters)

    @classmethod
    def __find_all(cls, filters: dict) -> list:
        """__find_all
        Busca todos los usuarios que hagan match con los filtros que
        se pasaron en los parametros

        Args:
            filters (dict): Filtros para los usuarios

        Returns:
            list: Todos los usuarios que se encontraron
        """
        try:
            mongo_users = cls.collection.find(filters)
            users = []
            for user in mongo_users:
                users.append(user)
            return users
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_all_user_info(cls, filters: dict):
        pipeline = [
            {"$match": filters},
            {
                "$lookup": {
                    "from": "companies",
                    "localField": "companies",
                    "foreignField": "rfc",
                    "as": "companies_info",
                }
            },
        ]
        try:
            user = cls.collection.aggregate(pipeline)
            if not user:
                raise Exception("No user found")
            return list(user)
        except Exception as e:
            raise Exception(e)
