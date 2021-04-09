"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene las rutas de los microservicios
"""
from flask import Blueprint, make_response, jsonify, request

from app import app
from app.service import user_service
from app.utils import validate_user, FilterType, make_filters

user_routes = Blueprint('user', __name__, url_prefix="/v1/user")


@user_routes.route("/all", methods=["GET"])
def get_users():
    """get_users
    Responde con una lista todos los usuarios que estan registrados en
    el sistema
    """
    users = user_service.get_users(make_filters(FilterType.AND, request.json))
    response = {}
    if not users:
        response = {"status": False, "users": []}
        return make_response(jsonify(response), 500)

    response = {"status": True, "users": users}
    return make_response(jsonify(response), 200)


@user_routes.route("/", methods=["POST"])
def save_user():
    """save_user
    Guarda el usuario que reciba en el request
    """
    user = request.json
    missing_fields = validate_user(user)
    if len(missing_fields) > 0:
        response = {
            "status": False, 
            "message": f"Faltan los siguientes campos: {f"{field}" for field in missing_fields}"
        }
        return make_response(jsonify(response), 404)
    
    if not user_service.add_user(user):
        response = {
            "status": False,
            "message": "No se pudo guardar el usuario en la base de datos"
        }
        return make_response(jsonify(response), 500)
    
    response = {
        "status": True,
        "id": user_service.get_user({"$and": [{"name": user["name"]}, {"email": user["email"]}]})._id
    }
    return make_response(jsonify(response), 200)



@user_routes.route("/", methods=["GET"])
def get_user():
    """get_user
    Obtiene un solo un usuario de la base de datos
    """
    filters = make_filters(FilterType.AND, request.json)
    user = user_service.get_user(filters)
    if not user:
        response = {
            "status": False,
            "message": "No se encontro al usuario que intentas buscar"
        }
        return make_response(jsonify(response), 404)
    
    response = {
        "status": True,
        "user": user
    }
    return make_response(jsonify(response), 200)


@user_routes.route("/", methods=["PUT"])
def update_user():
    """update_user(
    Actualiza un usuario en la base de datos
    """
    user = request.json
    if not user_service.update_user(user):
        response = {
            "status": False, 
            "message": f"No se pudo actualizar el usuario: {user._id}"
        }
        return make_response(jsonify(response), 404)
    response = {
        "status": True,
        "message": f"Se actualizo corretamente el usuario: {user._id}"
    }
    return make_response(jsonify(response), 200)


@user_routes.route("/", methods=["DELETE"])
def delete_user():
    """delete_user
    Elimina un usuario en la base de datos
    """
    user_id = request.json["_id"]
    if user_service.delete_user(user_id) != user_id:
        response = {
            "status": False, 
            "message": f"No se pudo eliminar el usuario: {user_id}"
        }
        return make_response(jsonify(response), 404)
    response = {
        "status": True,
        "message": f"Se elimino corretamente el usuario: {user_id}"
    }
    return make_response(jsonify(response), 200)

