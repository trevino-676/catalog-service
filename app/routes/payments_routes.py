from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps

from app.service import pay_service
from app import app

payment_routes = Blueprint("payment", __name__, url_prefix="/v1/payment")


@payment_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response


@payment_routes.route("/", methods=["GET"])
@cross_origin()
def find_payment():
    """
    Busca un solo complemento que coincida con el RFC
    """
    rfc = request.args["rfc"]
    message = ""
    try:
        payment = pay_service.get_pay({"Receptor.Rfc": rfc})
    except Exception as e:
        message = str(e)
        payment = None
    if payment is None:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": message
                    if message
                    else "No se encontro ningun complemento",
                }
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": payment}), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@payment_routes.route("/all", methods=["GET"])
@cross_origin()
def find_all_payments():
    """find_all_payments
    Busca todos los documentos que coincidan con los filtros
    """
    parameters = request.args
    filters = {}
    for k, v in parameters.items():
        if v == "null":
            filters[k] = None
        else:
            filters[k] = v

    app.logger.info(filters)
    payments = pay_service.get_pays(filters)

    if payments is None or len(payments) == 0:
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun recibo de payment"}
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": payments}), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp


@payment_routes.route("/get-group", methods=["POST"])
@cross_origin()
def find_data_basics():
    """
    Busca todos los documentos que coincidan con los filtros
    """

    parameters = request.form.to_dict()
    filters = {}
    message = ""
    for k, v in parameters.items():
        if v == "null":
            filters[k] = None
        else:
            filters[k] = v
    try:
        cfdis = pay_service.find_agg(
            [
                {
                    "$match": {
                        filters["fieldMatch"]: filters["user"],
                        "datos.Fecha": {
                            "$gte": filters["dateBegin"],
                            "$lte": filters["dateEnd"],
                        },
                    }
                },
                {"$group": {"_id": "$" + filters["fieldGroup"], "count": {"$sum": 1}}},
            ]
        )
    except Exception as e:
        print(e)
        message = str(e)
        cfdi = None
    if cfdis is None or len(cfdis) == 0:
        resp = make_response(
            dumps({"status": True, "data": []}),
            200,
        )
    else:
        resp = make_response(dumps({"status": True, "data": cfdis}), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp


@payment_routes.route("/get-count", methods=["POST"])
@cross_origin()
def data_count():
    """data_count
    Hace un conteo de los documentos que coincidan con los filtros
    """

    parameters = request.form.to_dict()
    if not "totalCol" in parameters:
        parameters["totalCol"] = "datos.Total"
    if not "subTotalCol" in parameters:
        parameters["subTotalCol"] = "datos.SubTotal"
    try:
        cfdis = pay_service.find_agg(
            [
                {
                    "$match": {
                        parameters["fieldMatch"]: parameters["user"],
                        "datos.Fecha": {
                            "$gte": parameters["dateBegin"],
                            "$lte": parameters["dateEnd"],
                        },
                        "datos.Cancelado": None,
                    }
                },
                {
                    "$project": {
                        parameters["fieldMatch"]: 1,
                        "count": {"$sum": 1},
                        "total": {"$sum": "$" + parameters["totalCol"]},
                        "subTotal": {"$sum": "$" + parameters["subTotalCol"]},
                    }
                },
                {
                    "$group": {
                        "_id": "$" + parameters["fieldMatch"],
                        "count": {"$sum": "$count"},
                        "total": {"$sum": "$total"},
                        "subTotal": {"$sum": "$subTotal"},
                    }
                },
            ]
        )
        if cfdis is None or len(cfdis) == 0:
            resp = make_response(
                dumps({"status": True, "data": []}),
                200,
            )
        resp = make_response(dumps({"status": True, "data": cfdis}), 200)
    except Exception as e:
        app.logger.error(e)
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun recibo de nomina"}
            ),
            404,
        )

    resp.headers["Content-Type"] = "application/json"
    return resp
