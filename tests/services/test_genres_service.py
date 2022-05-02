from unittest.mock import MagicMock

import pytest

from project.dao import GenreDAO
from project.dao.models import Genre
from project.services import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)
    genre1 = Genre(id=1, name="TestGenre1")
    genre2 = Genre(id=2, name="TestGenre2")

    genre_dao.get_by_id = MagicMock(return_value=genre1)
    genre_dao.get_all = MagicMock(return_value=[genre1, genre2])

    return genre_dao


class TestGenresService:
    @pytest.fixture(autouse=True)
    def service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_item_by_id(1)
        assert genre is not None
        assert genre['id'] is not None

    def test_get_all(self):
        genres = self.genre_service.get_all_genres()
        assert len(genres) > 0
