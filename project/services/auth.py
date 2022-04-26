import calendar
import datetime

import jwt
from flask import abort

from project.exceptions import ItemNotFound
from project.helpers.constants import JWT_SECRET, JWT_ALGORYTHM
from project.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, data):
        # access_token на 30 минут
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORYTHM)

        # refresh_token на 130 дней
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORYTHM)

        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens

    def refresh_tokens(self, req_json):
        refresh_token = req_json.get("refresh_token")
        ref_token = jwt.decode(refresh_token)
        if ref_token:
            tokens = self.generate_tokens(ref_token)
            return tokens, 200
        raise ItemNotFound