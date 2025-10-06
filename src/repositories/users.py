from sqlalchemy import select,insert
from .base import BaseRepository
from src.models.users import UsersModel
from src.schemas.users import User



class UserRepository(BaseRepository):
    model = UsersModel
    schema = User

    async def register(self, data_user):
        query = select(self.model.email).where(self.model.email == data_user["email"])
        result = await self.session.execute(query)
        if result.scalars().one_or_none() is not None:
            return {"message" : "The user already register"}
        stmt = insert(self.model).values(**data_user)
        await self.session.execute(stmt)