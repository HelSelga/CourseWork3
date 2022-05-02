import base64
import hashlib
import hmac

from flask import current_app

from project.helpers.constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT, JWT_SECRET, JWT_ALGORYTHM
from project.dao.user import UserDAO
from project.schemas.user import UserSchema


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_name(username)

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def create(self, user_d):
        user_d["password"] = self.make_user_password_hash(user_d.get("password"))
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = self.make_user_password_hash(user_d.get("password"))
        return self.dao.update(user_d)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_filter_users(self, page):
        limit = current_app.config["ITEMS_PER_PAGE"]
        offset = (page - 1) * limit
        users = self.dao.get_filter(limit=limit, offset=offset)
        return UserSchema(many=True).dump(users)

    def make_user_password_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256', other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)

    def update_password(self, email, new_password):

        user = self.get_by_email(email)
        user.password = new_password
        self.update(user)
