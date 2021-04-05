"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase para el modelo de usuarios
"""
from app import mongo, app
from app.model import DTO


class User(DTO):
    
    collection = mongo.db[app.config["DB_NAME"]]

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
            users = cls.collection.find(filters)
            if len(users) > 0:
                return users
            return None
        except Exception as e:
            print(e)
            return None