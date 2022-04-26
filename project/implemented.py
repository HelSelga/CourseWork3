from project.dao.director import DirectorDAO
from project.dao.genre import GenreDAO
from project.dao.movie import MovieDAO
from project.dao.user import UserDAO
from project.services.auth import AuthService
from project.services.directors_service import DirectorService
from project.services.genres_service import GenreService
from project.services.movies_service import MovieService
from project.services.user_service import UserService
from project.setup_db import db


director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
user_dao = UserDAO(session=db.session)

director_service = DirectorService(dao=director_dao)
genre_service = GenreService(dao=genre_dao)
movie_service = MovieService(dao=movie_dao)
user_service = UserService(dao=user_dao)
auth_service = AuthService(user_service)
