from flask import request
from flask_restx import Resource, Namespace, abort, reqparse
from project.exceptions import ItemNotFound

from project.helpers.decorators import auth_required
from project.implemented import user_service

users_ns = Namespace('users')

parser = reqparse.RequestParser()
parser.add_argument('page', type=int)


@users_ns.route('/')
class UsersView(Resource):
    @users_ns.expect(parser)
    @users_ns.response(200, "OK")
    @auth_required
    def get(self):
        page = parser.parse_args().get("page")
        if page:
            return user_service.get_filter_users(page)
        else:
            return user_service.get_all()


@users_ns.route('/<int:uid>')
class UserView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    @auth_required
    def get(self, uid: int):
        """Get user by id"""
        try:
            return user_service.get_one(uid)
        except ItemNotFound:
            abort(404, message="User not found")

    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def patch(self, uid: int):
        req_json = request.json
        if not req_json:
            abort(400, message='Bad Request')
        if "id" not in req_json:
            req_json["id"] = uid
        try:
            user_service.update(req_json)
        except ItemNotFound:
            abort(404, message="User not found")


@users_ns.route('/password/')
class UserPasswordView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    @auth_required
    def put(self):
        req_json = request.json

        if not req_json:
            abort(400, message='Bad Request')
        if not req_json.get("password1") or not req_json.get("password2"):
            abort(400, message='Bad Request')

        try:
            data = request.headers['Authorization']
            token = data.split("Bearer ")[-1]

            from project.helpers.constants import JWT_SECRET, JWT_ALGORYTHM
            import jwt

            token_decode = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORYTHM])
            user_service.update_password(email=token_decode['email'], new_password=req_json.get("password2"))

        except ItemNotFound:
            abort(404, message="User not found")
