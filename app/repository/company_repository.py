"""
author: Luis Manuel Torres Trevino
date: 18/05/2021
"""
from bson import ObjectId

from app import app
from app.model import Company
from app.repository import CompanyRepository


class CompanyMongoRepository(CompanyRepository):
    """
    En esta clase se definen lod metodos del repositorio de compania
    para la base de datos de MongoDB
    """

    def save(self, document: dict) -> bool:
        """
        Guarda una compania en la base de datos

        :params document (dict): Documento con los datos de la compania
        :return: True si el proceso fue un exito, False si hubo un error.
        """
        try:
            company = Company(document)
            company.save()
            app.logger.info(f"Se guardo correctamente la compania {company.name}")
            return True
        except Exception as e:
            app.logger.warning(e)
            return False

    def get_one(self, filter: dict) -> Company:
        """
        Busca la compania que coincida con los filtros

        :params filter (dict): filtros para buscar la compania.
        :return: La compania encontrada, si no se encuentra se manda
            un None
        """
        try:
            company = Company()
            company.find(filter)
            if str(company._id) == "":
                return None
            return company
        except Exception as e:
            app.logger.error(e)
            return None

    def get_all(self, filters: dict) -> list:
        """
        Busca todas las companias que coincidan con los filtros.

        :params filters (dict): filtros de busqueda

        :return: Lista con las companias encontradas. Si no se
            encuentran companias se envia un None.
        """
        try:
            companies = Company.find_companies(filters)
            if len(companies) == 0:
                return None
            return companies
        except Exception as e:
            app.logger.error(e)
            return None

    def update(self, document: dict) -> bool:
        """
        Actualiza la informacion de la compania que se pasa como
            parametro.

        :params document (dict): compania con los datos ya modificados

        :return: True si se actualizo de forma correcta, False si
            hubo un error durante el proceso.
        """
        if "_id" not in document:
            raise Exception("No se encuentra el _id de la compania")

        id = ObjectId(document["_id"])
        document["_id"] = id
        try:
            company = Company(document)
            company.save()
            return True
        except Exception as e:
            app.logger.error(e)
            return False

    def delete(self, id: str) -> str:
        """
        Elimina la compania del id que se envia como parametro

        :params id (str): id de la compania que se va a eliminar

        :return: id de la compania eliminada
        """
        if type(id) != str:
            raise Exception("El id debe de ser una cadena de texto")

        try:
            company = Company()
            company.find({"_id": ObjectId(id)})
            if str(company._id) != id:
                raise Exception("No se encontro la compania")

            company.remove()
            return id
        except Exception as e:
            app.logger.error(e)
            return ""
