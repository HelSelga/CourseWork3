from flask_restx import abort, Namespace, Resource, reqparse

from project.exceptions import ItemNotFound
from project.helpers.decorators import auth_required
from project.implemented import movie_service

movies_ns = Namespace("movies")

parser = reqparse.RequestParser()
parser.add_argument('page', type=int)
parser.add_argument('status', type=str)


@movies_ns.route("/")
class MoviesView(Resource):
    @auth_required
    @movies_ns.expect(parser)
    @movies_ns.response(200, "OK")
    def get(self):
        req_args = parser.parse_args()
        """Get all movies"""
        if any(req_args.values()):
            return movie_service.get_filter_movies(req_args)
        else:
            return movie_service.get_all_movies()


@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    @auth_required
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Movie not found")
    def get(self, mid: int):
        """Get movie by id"""
        try:
            return movie_service.get_item_by_id(mid)
        except ItemNotFound:
            abort(404, message="Movie not found")