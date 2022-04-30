from unittest.mock import Mock, patch, MagicMock

import pytest

from project.dao import GenreDAO
from project.dao.models import Genre
from project.exceptions import ItemNotFound
from project.schemas.genre import GenreSchema
from project.services import GenreService
from project.implemented import genre_service


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

    # @pytest.fixture
    # def genre(self):
    #     return Genre(id=1, name="genre_1")

    # @pytest.fixture
    # def genre_dao_mock(self, genre):
    #     with patch("project.services.genres_service.GenreDAO") as mock:
    #         mock.return_value = Mock(
    #             get_by_id=Mock(return_value=GenreSchema().dump(genre)),
    #             get_all=Mock(return_value=GenreSchema(many=True).dump([genre])),
    #         )
    #         yield mock

    # def test_get_all_genres(self, genre_dao_mock, genre):
    #     assert self.service.get_all_genres() == GenreSchema(many=True).dump([genre])
    #     genre_dao_mock().get_all.assert_called_once()
    #
    # def test_get_item_by_id(self, genre_dao_mock, genre):
    #     assert self.service.get_item_by_id(genre.id) == GenreSchema().dump(genre)
    #     genre_dao_mock().get_by_id.assert_called_once_with(genre.id)
    #
    # def test_get_item_by_id_not_found(self, genre_dao_mock):
    #     genre_dao_mock().get_by_id.return_value = None
    #
    #     with pytest.raises(ItemNotFound):
    #         self.service.get_item_by_id(1)

    def test_get_one(self):
        genre = self.genre_service.get_item_by_id(1)
        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all_genres()
        assert len(genres) > 0
