"""
author: ErrataSEV
date: 21/07/2021
"""
from app.model import Suppliers
from app.repository import SupplierRepository
from app import app


class SuppliersMongoRepository(SupplierRepository):
    def get_one(self, filters: dict) -> dict:
        """
        Busca el datos del proveedor en la base de datos
        :param filters: diccionario con los filtros de busqueda
        :return: diccionario con el documento encontrado.
        """
        print("Obj", filters)
        try:
            supplier = Suppliers()
            supplier.find(filters)
            app.logger.info(f"Se encontro el proveedor {str(supplier._id)}")
            return supplier
        except Exception as e:
            print("ERROR in repo", e)
            app.logger.error(e)
            return None

    def get_all(self, filters: dict) -> list:
        """
        Busca los proveedores de acuerdo a los filtros dados
        :param filters: diccionario con los filtros de busqueda
        :return: lista con todos los proveedores correspondientes
        """
        try:
            suppliers = Suppliers.find_all(filters)
            app.logger.info(f"Se encontraron {len(suppliers)} documentos")
            return suppliers
        except Exception as e:
            app.logger.error(e)
            return None

    def update_one(self, filters: str, field: dict):
        """
        Actualiza un documento en los campos establecidos
        :param rfc: RFC del proveedor a actualizar
        :return: UpdateResult o None en caso de error
        """
        try:
            suppliers = Suppliers.update_one(filters, field)
            app.logger.info(f"Respuesta {suppliers}")
            return suppliers
        except Exception as e:
            app.logger.error(e)
            return None

    def get_suppliers_by_company(self, rfc: str, filters: dict):
        try:
            suppliers = Suppliers.get_suppliers_by_company(rfc, filters)
            return suppliers
        except Exception as e:
            app.logger.error(e)
            return None
