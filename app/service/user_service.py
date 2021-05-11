"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la clase que implementa al servicio
"""
from app.repository import Repository
from app.service.service import Service


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
