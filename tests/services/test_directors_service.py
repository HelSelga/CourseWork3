from unittest.mock import MagicMock

import pytest

from project.dao import DirectorDAO
from project.dao.models import Director
from project.services import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)
    director_1 = Director(id=1, name="TestDirector11")
    director_2 = Director(id=2, name="TestDirector22")

    director_dao.get_by_id = MagicMock(return_value=director_1)
    director_dao.get_all = MagicMock(return_value=[director_1, director_2])

    return director_dao


class TestDirectorsService:
    @pytest.fixture(autouse=True)
    def service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_item_by_id(1)
        assert director is not None
        assert director['id'] is not None

    def test_get_all(self):
        director = self.director_service.get_all_directors()
        assert len(director) > 0
