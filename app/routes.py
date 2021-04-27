"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene las rutas de los microservicios
"""
from flask import Blueprint, make_response, jsonify, request
from bson.json_util import dumps

from app.service import user_service, upload_service
from app.utils import validate_user, FilterType, make_filters, validate_id
from app import app

user_routes = Blueprint('user', __name__, url_prefix="/v1/user")


@user_routes.route("/all", methods=["GET"])
def get_users():
    """get_users
    Responde con una lista todos los usuarios que estan registrados en
    el sistema
    """
    users = user_service.get_users(make_filters(FilterType.AND, request.json))
    if not users:
        response = {"status": False, "users": []}
        resp = make_response(jsonify(response), 500)
    else:
        response = {"status": True, "users": users}
        resp = make_response(dumps(response), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


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
            "message": f"Faltan los siguientes campos: "
                       f"{str(map(lambda field: field, missing_fields))}"
        }
        resp = make_response(jsonify(response), 404)
        resp.headers["Content-Type"] = "application/json"
        return resp

    if not user_service.add_user(user):
        response = {
            "status": False,
            "message": "No se pudo guardar el usuario en la base de datos"
        }
        resp = make_response(jsonify(response), 500)
    else:
        response = {
            "status": True,
            "id": "Se guardo correctamente el usuario"
        }
        resp = make_response(jsonify(response), 200)

    resp["Content-Type"] = "application/json"
    return resp


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
    resp = make_response(dumps(response), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/", methods=["PUT"])
def update_user():
    """update_user(
    Actualiza un usuario en la base de datos
    """
    user = request.json
    user["_id"] = validate_id(user["_id"])
    if not user_service.update_user(user):
        response = {
            "status": False,
            "message": f"No se pudo actualizar el usuario: {str(user['_id'])}"
        }
        resp = make_response(dumps(response), 404)
    else:
        response = {
            "status": True,
            "message": f"Se actualizo corretamente el usuario: {str(user['_id'])}"
        }
        resp = make_response(dumps(response), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/", methods=["DELETE"])
def delete_user():
    """delete_user
    Elimina un usuario en la base de datos
    """
    user_id = str(validate_id(request.json["_id"]))
    if user_service.delete_user(user_id) != user_id:
        response = {
            "status": False,
            "message": f"No se pudo eliminar el usuario: {str(user_id)}"
        }
        resp = make_response(jsonify(response), 404)
    else:
        response = {
            "status": True,
            "message": f"Se elimino corretamente el usuario: {str(user_id)}"
        }
        resp = make_response(jsonify(response), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/<rfc>/upload", methods=["POST"])
def upload_file(rfc):
    file = request.files["file"]
    file_type = "key" if file.filename.lower().endswith('.key') else "cer"

    if upload_service.upload_file(file, app.config["BUCKET"], rfc=rfc):
        resp = make_response(dumps({"status": True}), 200)
        user_service.update_files_user(rfc, file_type, file.filename)
    else:
        resp = make_response(dumps({"status": False}), 500)

    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/files/url", methods=["GET"])
def get_url_file():
    if "rfc" in request.json and "filename" in request.json:
        obj_name = f"{request.json['rfc']}/{request.json['filename']}"
    elif "file_route" in request.json:
        obj_name = request.json["file_route"]
    else:
        resp = make_response(
            dumps({"status": False, "message": "Los parametros enviados no son validos"}),
            404)
        resp.headers["Content-Type"] = "application/json"
        return resp

    url = upload_service.get_url(obj_name, app.config["BUCKET"])
    if url:
        resp = make_response(dumps({"status": True, "url": url}), 200)
    else:
        resp = make_response(dumps({"status": False, "url": ""}), 404)

    resp.headers["Content-Type"] = "application/json"
    return resp
