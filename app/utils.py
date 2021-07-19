"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene distintos metodos de uso general
    para el microservico de usuarios
"""
import jwt
from enum import Enum
from passlib.context import CryptContext

from bson import ObjectId


__pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000,
)


class FilterType(Enum):
    """FilterType
    Clase enum para los tipos de filtros
    """

    AND = 1
    OR = 2
    IN = 3


def validate_user(user: dict) -> list:
    """validate_user
    Valida el los campos del usuario que se manda por el request

    Args:
        user (dict): Usuario a validar

    Returns:
        list: Lista de campos faltantes obligatorios en el usuario
    """
    missing_fields = []
    if not "name" in user:
        missing_fields.append("name")
    elif not "last_name" in user:
        missing_fields.append("last_name")
    elif not "email" in user:
        missing_fields.append("email")
    elif not "password" in user:
        missing_fields.append("password")

    return missing_fields


def make_filters(type: FilterType, filters: dict) -> dict:
    """make_filters
    Genera un diccionario con los filtros para consultas de mongodb

    Args:
        type (FilterType): Tipo de filtro que se va a generar
        filters (dict): Datos que va a contener el filtro

    Returns:
        dict: Diccionario con la estructura aceptada por mongodb
    """
    new_filters = {}
    if type == FilterType.AND:
        new_filters = {"$and": [{item: value} for item, value in filters.items()]}
    elif type == FilterType.OR:
        new_filters = {"$or": [{item: value} for item, value in filters.items()]}
    elif type == FilterType.IN:
        new_filters = {item: {"$in": value} for item, value in filters.items()}
    else:
        raise Exception("The type isn't valid option")

    return new_filters


def validate_id(_id) -> str:
    """regresa el id del documento de mongo"""
    if type(_id) == dict:
        if "$oid" in _id:
            return ObjectId(_id["$oid"])
        else:
            return None
    else:
        return ObjectId(_id)


def encrypt_password(password: str):
    """
    Encripata la contraseña.

    :param password (str): contraseña que se va a encriptar
    :returns: Contraseña ya encriptada
    """
    return __pwd_context.encrypt(password)


def check_password(password, hash_passwd):
    """
    Compara la contraseña con la contraseña ya encriptada.

    :param password (str): Contrasena sin encriptar.
    :param hash_passwd (str): Contrasena encriptada.
    :returns: True si coinciden, False si no.
    """
    return __pwd_context.verify(password, hash_passwd)


def decode_token(token, secret_key, encrypt_method="SHA256"):
    """
    Decodifica el token de autenticacion
    """
    return jwt.decode(token, secret_key, algorithms=encrypt_method)
