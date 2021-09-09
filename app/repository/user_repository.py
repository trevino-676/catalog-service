"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene la implementacion del repositorio
    de usuarios

TODO: Agregar los logs a las acciones de los usuarios.
"""
from bson import ObjectId

from app.model import User
from app.repository import Repository


class UserMongoRepository(Repository):
    def save_user(self, user: dict) -> bool:
        """save_user
        Guarda un nuevo usuario en la base de datos

        Args:
            user (dict): diccionario con los datos del usuario que se
                va a crear.

        Returns:
            bool: booleano indicando si se guardo el usuario o no
        """
        try:
            new_user = User(user)
            new_user.save()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user(self, filters: dict) -> User:
        """get_user
        Busca un usuario dentro de la base de datos, el usuario debe
        coincidir con los filtros

        Args:
            filters (dict): diccionario con los filtros.

        Returns:
            User: Una instancia con el usuario encontrado.
        """
        try:
            user = User(User.find_all_user_info(filters)[0])
            if str(user._id) == "":
                return None
            return user
        except Exception:
            return None

    def get_users(self, filters: dict) -> list:
        """get_users
        Busca a los usuarios que coinciden con los filtros en la base
        de datos.

        Args:
            filters (dict): diccionario con los filtros

        Returns:
            list: Todos los usuarios que concuerdan con los filtros
        """
        return User.get_all_users(filters)

    def update_user(self, user: dict) -> bool:
        """update_user
        Actualiza la informacion del usuario que se pasa como parametros.

        Params:
            user (dict): diccionario con los datos del usuario.ƒƒ

        Returns:
            bool: bandera que indica si se guardo correctamente o no.
        """
        try:
            new_user = User(user)
            new_user.save()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_user(self, id: str) -> str:
        """delete_user
        Borra el usario que contenga el id del parametro

        Params:
            id (str): id del usuario.

        Returns:
            str: id del usuario eliminado.
        """
        try:
            user = User()
            user.find({"_id": ObjectId(id)})
            if not user._id:
                return ""
            user.remove()
            return id
        except Exception as e:
            print(e)
            return ""

    def find_agg(self, filters: list):
        """
        Realiza una busqueda con aggregate
        :param filters: lista de 'Stages' del aggregate
        :return: uknown
        """
        try:
            config_model = User.find_agg(filters)
            return config_model
        except Exception as e:
            print(e)
            return None

