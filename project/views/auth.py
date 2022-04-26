from flask import request, abort
from flask_restx import Namespace, Resource

from project.exceptions import ItemNotFound
from project.implemented import auth_service, user_service
from project.tools.security import login_user

auth_ns = Namespace('auth')


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        if not req_json:
            abort(400, message='Bad Request')

        try:
            user = user_service.get_by_email(email=req_json.get("email"))
            tokens = login_user(req_json, user)
            return tokens, 200
        except ItemNotFound:
            abort(401, message='Authorization Error')

    def put(self):
        req_json = request.json
        if not req_json:
            abort(400, message='Bad Request')
        try:
            tokens = auth_service.refresh_tokens(req_json)
            return tokens, 200
        except ItemNotFound:
            abort(401, message='Authorization Error')


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        req_json = request.json
        if not req_json:
            abort(400, message='Bad Request')
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}