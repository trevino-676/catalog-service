from flask import Blueprint, request, make_response
from flask_cors import cross_origin
from bson.json_util import dumps

from app.service import upload_service
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
