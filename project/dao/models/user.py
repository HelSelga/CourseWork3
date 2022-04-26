from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = 'users'

    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    favorite_genre = db.Column(db.String)

    def __repr__(self):
        return f"<User '{self.email.title()}'>"
