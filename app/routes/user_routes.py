"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene las rutas de los microservicios
"""
from flask import Blueprint, make_response, jsonify, request
from flask_cors import cross_origin
from flask_jwt import jwt_required, current_identity
from bson.json_util import dumps

from app.service import user_service, upload_service, config_service
from app.utils import (
    FilterType,
    make_filters,
    validate_id,
    encrypt_password,
)
from app import app

user_routes = Blueprint("user", __name__, url_prefix="/v1/user")


@user_routes.route("/all", methods=["GET"])
@cross_origin()
@jwt_required()
def get_users():
    """get_users
    Responde con una lista todos los usuarios que estan registrados en
    el sistema
    """
    request_filters = request.args.get("filters")
    request_filter_type = request.args.get("type")
    parameters = None
    if request_filter_type and request_filters:
        parameters = {"type": request_filter_type, "filters": request_filters}

    if parameters is None:
        filters = {}
    else:
        if parameters["type"] == "in":
            filters = make_filters(FilterType.IN, parameters["filters"])
        elif parameters["type"] == "and":
            filters = make_filters(FilterType.AND, parameters["filters"])
        else:
            filters = make_filters(FilterType.OR, parameters["filters"])

    users = user_service.get_users(filters)
    if not users:
        resp = make_response(
            dumps({"status": False, "message": "No se encontraron usuarios"}), 404
        )
    resp = make_response(dumps({"status": False, "users": users}), 200)
    return resp


@user_routes.route("/", methods=["POST"])
@cross_origin()
def save_user():
    """save_user
    Guarda el usuario que reciba en el request
    """
    user = request.json
    user["password"] = encrypt_password(user["password"])
    if not user_service.add_user(user):
        response = {
            "status": False,
            "message": "No se pudo guardar el usuario en la base de datos",
        }
        resp = make_response(jsonify(response), 500)
    else:
        new_user = user_service.get_user({"name": user["name"], "email": user["email"]})
        if config_service.add({"user": str(new_user["_id"]), "wizzard": True}):
            response = {"status": True, "id": "Se guardo correctamente el usuario"}
            resp = make_response(jsonify(response), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp


# TODO: Cambiar forma de obtener los parametros del request
@user_routes.route("/", methods=["GET"])
@cross_origin()
@jwt_required()
def get_user():
    """get_user
    Obtiene un solo un usuario de la base de datos
    """
    filters = make_filters(FilterType.AND, request.json)
    user = user_service.get_user(filters)
    if not user:
        response = {
            "status": False,
            "message": "No se encontro al usuario que intentas buscar",
        }
        return make_response(jsonify(response), 404)
    response = {"status": True, "user": user}
    resp = make_response(dumps(response), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/", methods=["PUT"])
@cross_origin()
@jwt_required()
def update_user():
    """update_user(
    Actualiza un usuario en la base de datos
    """
    user = request.json
    user["_id"] = validate_id(user["_id"])
    if not user_service.update_user(user):
        response = {
            "status": False,
            "message": f"No se pudo actualizar el usuario: {str(user['_id'])}",
        }
        resp = make_response(dumps(response), 404)
    else:
        response = {
            "status": True,
            "message": f"Se actualizo corretamente el usuario: {str(user['_id'])}",
        }
        resp = make_response(dumps(response), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/", methods=["DELETE"])
@cross_origin()
@jwt_required()
def delete_user():
    """delete_user
    Elimina un usuario en la base de datos
    """
    user_id = validate_id(request.args.get("id"))
    config = config_service.get_one({"user": str(user_id)})
    config_service.delete(str(config["_id"]))
    if user_service.delete_user(user_id) != user_id:
        response = {
            "status": False,
            "message": f"No se pudo eliminar el usuario: {str(user_id)}",
        }
        resp = make_response(jsonify(response), 404)
    else:
        response = {
            "status": True,
            "message": f"Se elimino corretamente el usuario: {str(user_id)}",
        }
        resp = make_response(jsonify(response), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/<rfc>/upload", methods=["POST"])
@cross_origin()
@jwt_required()
def upload_file(rfc):
    file = request.files["file"]
    file_type = "key" if file.filename.lower().endswith(".key") else "cer"

    if upload_service.upload_file(file, app.config["BUCKET"], rfc=rfc):
        resp = make_response(dumps({"status": True}), 200)
        user_service.update_files_user(rfc, file_type, file.filename)
    else:
        resp = make_response(dumps({"status": False}), 500)

    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/files/url", methods=["GET"])
@cross_origin()
@jwt_required()
def get_url_file():
    if "rfc" in request.json and "filename" in request.json:
        obj_name = f"{request.json['rfc']}/{request.json['filename']}"
    elif "file_route" in request.json:
        obj_name = request.json["file_route"]
    else:
        resp = make_response(
            dumps({"status": False, "message": "Los parametros enviados no son validos"}),
            404,
        )
        resp.headers["Content-Type"] = "application/json"
        return resp

    url = upload_service.get_url(obj_name, app.config["BUCKET"])
    if url:
        resp = make_response(dumps({"status": True, "url": url}), 200)
    else:
        resp = make_response(dumps({"status": False, "url": ""}), 404)

    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/fiel", methods=["POST"])
@cross_origin()
@jwt_required()
def set_fiel_password():
    params = request.json

    if "_id" not in params and "rfc" not in params:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": "No se encuentra el _id o rfc de usuario en parametros",
                }
            ),
            404,
        )

    filter = {"rfc": params["rfc"]}
    if user_service.set_fiel_password(filter, params["fiel"]):
        resp = make_response(
            dumps({"status": True, "message": "Contrasena guardada"}), 200
        )
    else:
        resp = make_response(
            dumps({"status": False, "message": "Problemas al guardar la contrasena"}),
            500,
        )

    resp.headers["Content-Type"] = "application/json"
    return resp


@user_routes.route("/login", methods=["POST"])
@cross_origin()
def login_user():
    params = request.json
    if "email" not in params or "password" not in params:
        return make_response(
            dumps(
                {
                    "status": False,
                    "message": "Los datos de la peticion no son correctos",
                },
            ),
            500,
        )
    if not user_service.login(params["email"], params["password"]):
        return make_response(
            dumps({"status": False, "message": "Usuario o contrasena incorrectos"}), 404
        )
    return make_response(dumps({"status": True, "data": {"token": ""}}), 200)


@user_routes.route("/logged_info", methods=["GET"])
@cross_origin()
@jwt_required()
def get_logged_info():
    """
    Returns the user info how is logged
    """
    user = current_identity
    return make_response(dumps({"status": True, "user": user}), 200)


@user_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
