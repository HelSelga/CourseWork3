from project.dao.models.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).filter(User.id == uid).one_or_none()

    def get_by_name(self, name):
        return self.session.query(User).filter(User.name == name).first()

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        if "name" in user_d:
            user.name = user_d.get("name")
        if "surname" in user_d:
            user.surname = user_d.get("surname")
        if "favorite_genre" in user_d:
            user.favorite_genre = user_d.get("favorite_genre")

        self.session.add(user)
        self.session.commit()

    def get_filter(self, limit, offset):
        return self.session.query(User).limit(limit).offset(offset).all()
