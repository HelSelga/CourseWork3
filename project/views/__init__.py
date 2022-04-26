from .genres import genres_ns
from .auth import auth_ns
from .users import users_ns
from .directors import directors_ns
from .movies import movies_ns

__all__ = [
    "genres_ns",
    "movies_ns",
    "directors_ns",
    "auth_ns",
    "users_ns"
]
