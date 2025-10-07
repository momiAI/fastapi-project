from sqlalchemy import select,insert
from .base import BaseRepository
from src.models.users import UsersModel
from src.schemas.users import User



class UserRepository(BaseRepository):
    model = UsersModel
    schema = User

    async def register(self, data_user):
        stmt = insert(self.model).values(**data_user)
        await self.session.execute(stmt)