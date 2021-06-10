"""
author: Luis Manuel Torres Trevino
date: 19/05/2021
"""
from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps
from flask_jwt import jwt_required

from app import app
from app.service import company_service
from app.utils import validate_user, make_filters, validate_id, FilterType


company_routes = Blueprint("company", __name__, url_prefix="/v1/company")


@company_routes.route("/", methods=["POST"])
@jwt_required()
@cross_origin()
def create_company():
    """
    Crea una nueva compania en la base de datos
    """
    if "company" not in request.json:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": "La estructura de la peticion es incorrecta",
                }
            ),
            500,
        )
        return resp

    company = request.json["company"]
    if not company_service.add(company):
        resp = make_response(
            dumps({"status": False, "message": "Error al guardar la compania"}), 500
        )
        return resp
    resp = make_response(
        {"status": True, "message": "Compania creada correctamente"}, 200
    )

    return resp


@company_routes.route("/", methods=["GET"])
@jwt_required()
@cross_origin()
def get_company():
    """
    Busca y devuelve una compania
    """
    if "type" not in request.json or "filters" not in request.json:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": "La estructura de la peticion es incorrecta",
                }
            ),
            500,
        )
        return resp

    filter_type = request.json["type"]
    filters = make_filters(
        FilterType.AND if filter_type == "and" else FilterType.OR,
        request.json["filters"],
    )
    company = company_service.get_one(filters)
    if not company:
        resp = make_response(
            dumps({"status": False, "message": "No se encontro compania"}), 404
        )
        return resp

    resp = make_response(dumps({"status": True, "company": company}), 200)
    return resp


@company_routes.route("/all", methods=["GET"])
@jwt_required()
@cross_origin()
def get_companies():
    """
    Buscay devuelve una lista de companias
    """
    parameters = request.json
    app.logger.info(parameters)
    if parameters is None:
        filters = {}
    else:
        if "type" not in parameters or "filters" not in parameters:
            filters = {}
        else:
            filter_type = request.json["type"]
            if filter_type == "in":
                filters = make_filters(FilterType.IN, request.json["filters"])
            else:
                filters = make_filters(
                    FilterType.AND if filter_type == "and" else FilterType.OR,
                    request.json["filters"],
                )
    companies = company_service.get_all(filters)
    if not companies:
        resp = make_response(
            dumps({"status": False, "message": "No se encontro companias"}), 404
        )
        return resp

    resp = make_response(dumps({"status": True, "companies": companies}), 200)
    return resp


@company_routes.route("/", methods=["PUT"])
@jwt_required()
@cross_origin()
def update_company():
    """
    Actualiza una compania
    """
    if "company" not in request.json:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": "La estructura de la peticion es incorrecta",
                }
            ),
            500,
        )
        return resp
    if not company_service.update(request.json["company"]):
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": "Hubo un problema al actualizar la compania",
                }
            ),
            500,
        )
        return resp
    resp = make_response(
        {"status": True, "message": "Compania actualizada correctamente"}, 200
    )

    return resp


@company_routes.route("/<id>", methods=["DELETE"])
@jwt_required()
@cross_origin()
def delete_company(id):
    """
    Borra la compania que se pasa como parametro
    """
    deleted_id = company_service.delete(id)
    if deleted_id != id:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": "Hubo un problema al borrar la compania",
                }
            ),
            500,
        )
        return resp
    resp = make_response(
        {"status": True, "message": "Compania actualizada correctamente"}, 200
    )

    return resp


@company_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response