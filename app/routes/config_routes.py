import json

from flask import Blueprint, request, make_response
from flask_jwt import jwt_required, current_identity
from flask_cors import cross_origin

from app.service import config_service, user_service


config_routes = Blueprint("config", __name__, url_prefix="/v1/config")


@config_routes.route("/", methods=["POST"])
@cross_origin()
@jwt_required()
def new_config():
    config = request.json
    config["user"] = str(current_identity["_id"])
    if not config_service.add(config):
        return make_response(json.dumps({"staus": False}), 500)
    return make_response(json.dumps({"status": True}), 200)


@config_routes.route("/", methods=["GET"])
@cross_origin()
@jwt_required()
def get_config():
    id = str(current_identity["_id"])
    config = config_service.get_one({"user": id})
    if not config:
        return make_response(json.dumps({"status": False}), 404)
    config["_id"] = str(config["_id"])
    return make_response(json.dumps({"status": True, "data": config}))


@config_routes.route("/", methods=["PUT"])
@cross_origin()
@jwt_required()
def update_config():
    config = request.json
    if not config_service.update(config):
        return make_response(json.dumps({"status": False}), 500)
    return make_response(json.dumps({"status": True}), 200)


@config_routes.route("/<id>", methods=["DELETE"])
@cross_origin()
@jwt_required()
def delete_config(id: str):
    if not config_service.delete(id):
        return make_response(json.dumps({"status": False}), 500)
    return make_response(json.dumps({"status": True}), 200)


@config_routes.route("/company-config", methods=["POST"])
@cross_origin()
def find_data_basics():
    """
    Busca todos los documentos que coincidan con los filtros
    """

    parameters = request.form.to_dict()
    try:
        cfdis = user_service.aggregate(
            [
                {"$match": {"companies": parameters["rfc"]}},
                {"$addFields": {"usr_id": {"$toString": "$_id"}}},
                {
                    "$lookup": {
                        "from": "config",
                        "localField": "usr_id",
                        "foreignField": "user",
                        "as": "config_usr",
                    }
                },
                {"$project": {"_id": 0, "config_usr._id": 0}},
            ]
        )
        print(cfdis)
    except Exception as e:
        print(e)
        cfdis = None
    if cfdis is None or len(cfdis) == 0:
        resp = make_response(
            json.dumps({"status": True, "data": []}),
            200,
        )
    else:
        resp = make_response(
            json.dumps({"status": True, "data": cfdis[0]["config_usr"]}), 200
        )

    resp.headers["Content-Type"] = "application/json"
    return resp


@config_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response
