from sqlalchemy import desc

from project.dao.models.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).filter(Movie.id == mid).first()

    def get_all(self):
        return self.session.query(Movie).all()

    def get_filter(self, limit, offset, status):
        if limit > 0 and status == "new":
            return self.session.query(Movie).order_by(desc(Movie.year)).limit(limit).offset(offset).all()
        elif limit > 0:
            return self.session.query(Movie).limit(limit).offset(offset).all()
        elif status == "new":
            return self.session.query(Movie).order_by(desc(Movie.year)).all()
