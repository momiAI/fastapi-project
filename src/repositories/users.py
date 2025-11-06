from .base import BaseRepository
from src.models.users import UsersModel
from src.repositories.mappers.mappers import UserMapper


class UserRepository(BaseRepository):
    model = UsersModel
    mapper = UserMapper

