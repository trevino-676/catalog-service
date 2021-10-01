from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from flask_jwt import jwt_required, current_identity
from bson.json_util import dumps

from app.service import account_service


account_routes = Blueprint("accounts", __name__, url_prefix="/v1/account")
ERROR_MESSAGE = "Hubo un error al {} la cuenta";
ERROR_FIND_MESSAGE = "No se encontraron cuentas que coincidan con los filtros"
SUCCESS_MESSAGE = "Se {} la cuenta correctamente"


@account_routes.route("/", methods=["POST"])
@cross_origin()
@jwt_required()
def create_account():
    account = request.json
    if not account_service.add(account):
        return make_response(
            dumps({"status": False, "message": ERROR_MESSAGE.format("crear")}),
            500
        )
    return make_response(
        dumps({"status": True, "message": SUCCESS_MESSAGE.format("creo")}),
        200
    )


@account_routes.route("/", methods=["GET"])
@cross_origin()
@jwt_required()
def find_count():
    filters = dict(request.args)
    account = account_service.get_one(filters)
    if not account:
        return make_response(
            dumps({"status": False, "message": ERROR_FIND_MESSAGE}),
            404
        )
    return make_response(dumps({"status": True, "data": account}), 200)


@account_routes.route("/by_user", methods=["GET"])
@cross_origin()
@jwt_required()
def find_accounts_by_user():
    companies = current_identity["companies"]
    filters = {"company": {"$in": companies}}
    accounts = account_service.get_all(filters)
    if not accounts:
       return make_response(
            dumps({"status": False, "message": ERROR_FIND_MESSAGE}),
            404
        )
    return make_response(dumps({"status": True, "data": accounts}), 200)


@account_routes.route("/", methods=["PUT"])
@cross_origin()
@jwt_required()
def update_account():
    account = request.json
    if not account_service.update(account):
        return make_response(
            dumps({"status": False, "message": ERROR_MESSAGE.format("actualizar")}),
            500
        )
    return make_response(
        dumps({"status": True, "message": SUCCESS_MESSAGE.format("actualizo")}),
        200
    )


@account_routes.route("/", methods=["DELETE"])
@cross_origin()
@jwt_required()
def delete_account():
    id = str(request.args.get("id"))
    if not account_service.delete(id):
        return make_response(
            dumps({"status": False, "message": ERROR_MESSAGE.format("eliminar")}),
            500
        )
    return make_response(
        dumps({"status": True, "message": SUCCESS_MESSAGE.format("elimino")}),
        200
    )



@account_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
