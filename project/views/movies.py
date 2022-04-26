from flask_restx import abort, Namespace, Resource, reqparse

from project.exceptions import ItemNotFound
from project.services.movies_service import MovieService
from project.setup_db import db

movies_ns = Namespace("movies")

parser = reqparse.RequestParser()
parser.add_argument('page', type=int)
parser.add_argument('status', type=str)


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.expect(parser)
    @movies_ns.response(200, "OK")
    def get(self):
        req_args = parser.parse_args()
        """Get all movies"""
        if any(req_args.values()):
            return MovieService(db.session).get_filter_movies(req_args)
        else:
            return MovieService(db.session).get_all_movies()


@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Movie not found")
    def get(self, mid: int):
        """Get movie by id"""
        try:
            return MovieService(db.session).get_item_by_id(mid)
        except ItemNotFound:
            abort(404, message="Movie not found")