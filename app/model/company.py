"""
author: Luis Manuel Torres Trevino
date: 18/05/2021
"""
from app.model import DTO
from app import app, mongo


class Company(DTO):
    """
    Clase modelo para las compamnias
    """

    collection_name = app.config["COMPANY_COLLECTION"]
    collection = mongo[collection_name]

    def __get_all_companies(cls, filters: dict) -> list:
        """
        Este metodo busca todas las companias que coincidan con los
        filtros que se pasan como parametros

        :param filters (dict): Diccionario con los filtros para la
            busqueda.
        :return: Lista con todos las companias encontradas
        """
        try:
            companies = cls.collection.find(filters)
            return companies
        except Exception as e:
            app.logger.error(e.message)
            return None

    @classmethod
    def find_companies(cls, filters: dict) -> list:
        return cls.__get_all_companies(filters)
