import hashlib

from flask import current_app

from project.exceptions import ItemNotFound
from project.implemented import user_service, auth_service


def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def login_user(req_json, user):
    email = req_json.get("email")
    password = req_json.get("password")
    if email and password:
        password_hash = user["password"]
        req_json["role"] = user["role"]
        req_json["id"] = user["id"]
        if user_service.compare_passwords(password_hash, password):
            return auth_service.generate_tokens(req_json)
        raise ItemNotFound


