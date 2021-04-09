"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene distintos metodos de uso general
    para el microservico de usuarios
"""
from enum import Enum


class FilterType(Enum):
    """FilterType
    Clase enum para los tipos de filtros
    """

    AND = 1
    OR = 2


def validate_user(user: dict) -> list:
    """validate_user
    Valida el los campos del usuario que se manda por el request

    Args:
        user (dict): Usuario a validar

    Returns:
        list: Lista de campos faltantes obligatorios en el usuario
    """
    missing_fields = []
    if not user["name"] or not user["nombre"]:
        missing_fields.append("name")
    elif not user["last_name"] or not user["apellidos"]:
        missing_fields.append("last_name")
    elif not user["password"] or not user["contrasena"]:
        missing_fields.append("password")
    elif not user["email"] or not user["mail"] or not user["correo_electronico"]:
        missing_fields.append("email")

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
    else:
        raise Exception("The type isn't valid option")

    return new_filters