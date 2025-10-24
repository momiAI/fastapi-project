from sqlalchemy import select,insert
from .base import BaseRepository
from src.models.users import UsersModel
from src.schemas.users import User
from src.repositories.mappers.mappers import UserMapper


class UserRepository(BaseRepository):
    model = UsersModel
    mapper = UserMapper

    async def register(self, data_user):
        stmt = insert(self.model).values(**data_user)
        await self.session.execute(stmt)