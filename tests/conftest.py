from unittest.mock import MagicMock

import pytest

from project.config import TestingConfig
from project.dao import GenreDAO, DirectorDAO
from project.dao.models import Genre, Director
from project.server import create_app
from project.setup_db import db as database


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()

    yield database

    database.session.rollback()


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client




@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)
    cris = Director(id=21, name="Christina Robes")
    sam = Director(id=22, name="Samuel Jackson")
    dina = Director(id=23, name="Dina Stores")

    director_dao.get_one = MagicMock(return_value=cris)
    director_dao.get_all = MagicMock(return_value=[cris, sam, dina])

    return director_dao

