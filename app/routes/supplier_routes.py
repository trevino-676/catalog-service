from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps

from app.service import upload_service, suppliers_service
from app import app

supplier_routes = Blueprint("supplier", __name__, url_prefix="/v1/supplier")


@supplier_routes.route("/opinion/<rfc>/upload", methods=["POST"])
@cross_origin()
def upload_opinion(rfc):
    file = request.files["file"]
    dir_name = f"opinion/{rfc}"

    if upload_service.upload_file(file, app.config["BUCKET"], rfc=dir_name):
        return make_response((dumps({"status": True})), 200)
    return make_response(dumps({"status": False}), 500)


@supplier_routes.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Type"] = "application/json"
    return response


@supplier_routes.route("/", methods=["GET"])
def find_supplier():
    """
    Busca un solo proveedor que coincida con el RFC
    """
    rfc = request.args["rfc"]
    print("req", rfc)
    try:
        supplier = suppliers_service.get_supp({"_id": rfc})
    except Exception as e:
        message = str(e)
        supplier = None
    if supplier is None:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": message if message else "No se encontro ningun proveedor",
                }
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": supplier}), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@supplier_routes.route("/all", methods=["GET"])
def find_all_suppliers():
    """find_all_suppliers
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
    suppliers = suppliers_service.get_supps(filters)

    if suppliers is None or len(suppliers) == 0:
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun recibo de supplier"}
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": suppliers}), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp


@supplier_routes.route("/set", methods=["POST"])
def update_one():
    """
    Actualiza campos de un proveedor
    """
    parameters = request.form.to_dict()
    rfc = ""
    fields = {}
    try:
        rfc = parameters["rfc"]
        parameters.pop("rfc")
        for k, v in parameters.items():
            if v == "null":
                fields[k] = None
            else:
                fields[k] = bool(v)
    except Exception as e:
        app.logger.error(e)
        fields = None

    if fields is None:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": "No se encontro ningun proveedor",
                }
            ),
            404,
        )

    res = suppliers_service.update_one(rfc, fields)

    if res is None:
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun recibo de supplier"}
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": res.raw_result}), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp