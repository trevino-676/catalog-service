from functools import wraps
import time
import jwt
from flask import request, jsonify, make_response

from app.routes.user_routes import user_routes
from app.routes.company_routes import company_routes
from app import app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return make_response({"message": "Falta token de autenticacion"}, 403)
        
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithm = 'HS256')
        except Exception as e:
            app.logger.error(e)
            return make_response({"message": "Token invalido"}, 403)
        
        return f(*args, **kwargs)
    
    return decorated