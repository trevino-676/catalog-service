"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase que implementa al servicio
"""
from app.repository import Repository
from app.service.service import Service
from app.utils import check_password
from app.model import User


class UserService(Service):
    def __init__(self, repository: Repository):
        self.repository = repository

    def add_user(self, user: dict) -> bool:
        return self.repository.save_user(user)

    def get_user(self, filters: dict):
        return self.repository.get_user(filters)

    def get_users(self, filters: dict) -> list:
        return self.repository.get_users(filters)

    def update_user(self, user: dict) -> bool:
        return self.repository.update_user(user)

    def delete_user(self, id: str) -> str:
        return self.repository.delete_user(id)

    def update_files_user(self, rfc: str, document_type: str, filename: str):
        """Actualiza el usuario con las rutas de los archivos que se
        guardaron en el storage

        :param rfc: rfc del usuario.
        :param document_type: Tipo de documento.
        :param filename: Nombre del archivo dentro del storage
        """
        user = self.repository.get_user({"rfc": rfc})
        user[document_type] = f"{rfc}/{filename}"
        user.save()

    def set_fiel_password(self, filters, fiel_password):
        try:
            user = self.repository.get_user(filters)
            user["fiel"] = fiel_password
            user.save()
            return True
        except Exception as e:
            print(e)
            return False

    def login(self, email, password) -> dict:
        """Loggea al usuario en el sistema"""
        filter = {"email": email}
        user = self.get_user(filter)
        if not user:
            return None

        return check_password(password, user["password"])

    @classmethod
    def add_companies_to_user(cls, user, company_rfc):
        """Agrega una nueva compania al usuario

        Params:
            company_rfc (str): rfc de la compania nueva.

        Returns:
            True si se guardo correctamente.

        Raise:
            Exception: Si hubo un error al guardar la informacion.
        """
        if "companies_info" in user:
            del user["companies_info"]
        if "companies" not in user:
            user["companies"] = [company_rfc]
        else:
            rfc_exists = list(filter(lambda rfc: (rfc == company_rfc), user["companies"]))
            if not rfc_exists:
                user["companies"].append(company_rfc)

        updated_user = User(user)
        try:
            updated_user.save()
            return True
        except Exception as e:
            raise Exception(e)

    @classmethod
    def delete_companies_of_user(cls, user: dict, company_rfc: str) -> bool:
        """Elimina la compania de la lista de companias del usuario

        Params:
            user (dict): Diccionario con los datos del usuario.
            company_rfc (str): Rfc de la compania que se va eliminar.

        Returns:
            True si se elimino correctamente.
        """
        if "companies" not in user:
            raise Exception("The list of companies doesn't exist in the user")

        updated_user = User(user)
        rfc_exists = list(
            filter(lambda rfc: (rfc == company_rfc), updated_user.companies)
        )

        if not rfc_exists:
            raise Exception("The company rfc doesn't exist in the companies list")

        updated_user.companies.remove(company_rfc)

        try:
            updated_user.save()
            return True
        except Exception as e:
            raise Exception(e)

    def aggregate(self, filters: list):
        return self.repository.find_agg(filters)
