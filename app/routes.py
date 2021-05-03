"""
author: Luis Manuel Torres Trevino
description: Este archivo contiene las rutas de los microservicios
"""
from flask import Blueprint, make_response, jsonify, request
from bson.json_util import dumps

from app.service import user_service
from app.utils import validate_user, FilterType, make_filters

##########################
from functools import wraps
import time 
import jwt #PyJWT==1.7.1 
import datetime  
##########################

user_routes = Blueprint('user', __name__, url_prefix="/v1/user")

###########################jlb
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not token: 
            return jsonify({'message' : 'falta token!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithm = 'HS256')
        except:
            return jsonify({'message' : 'Token inválido!'}), 403

        return f(*args, **kwargs)

    return decorated 
"""
@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'abierto'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message' : 'protegido'})""" 
###########################jlg

############################jlb 
@user_routes.route('/login')
def login():
    auth = request.authorization
    tm = int(time.time())
    if auth and auth.password == 'secret':
        token = jwt.encode({'user' : 'try', 'nombre' : 'name', 'time' : tm }, app.config['SECRET_KEY'], 
                algorithm = 'HS256')
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('No se puede verificar!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
############################jlb 

@user_routes.route("/all", methods=["GET"])
def get_users():
    """get_users
    Responde con una lista todos los usuarios que estan registrados en
    el sistema
    """
    users = user_service.get_users(make_filters(FilterType.AND, request.json))
    if not users:
        response = {"status": False, "users": []}
        return make_response(jsonify(response), 500)

    response = {"status": True, "users": users}

    return make_response(dumps(response), 200)


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
            "message": f"Faltan los siguientes campos: {str(map(lambda field : field, missing_fields))}"
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
        "id": "Se guardo correctamente el usuario"
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
    return make_response(dumps(response), 200)


@user_routes.route("/", methods=["PUT"])
def update_user():
    """update_user(
    Actualiza un usuario en la base de datos
    """
    user = request.json
    if not user_service.update_user(user):
        response = {
            "status": False, 
            "message": f"No se pudo actualizar el usuario: {str(user._id)}"
        }
        return make_response(jsonify(response), 404)
    response = {
        "status": True,
        "message": f"Se actualizo corretamente el usuario: {str(user._id)}"
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
            "message": f"No se pudo eliminar el usuario: {str(user_id)}"
        }
        return make_response(jsonify(response), 404)
    response = {
        "status": True,
        "message": f"Se elimino corretamente el usuario: {str(user_id)}"
    }
    return make_response(jsonify(response), 200)

