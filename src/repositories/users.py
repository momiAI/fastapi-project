from sqlalchemy import select

from .base import BaseRepository
from src.models.users import UsersModel
from src.repositories.utils import check_valid_number
from src.repositories.mappers.mappers import UserMapper


class UserRepository(BaseRepository):
    model = UsersModel
    mapper = UserMapper

    async def check_number(self, phone_number):
        print(phone_number)
        check_number_in_correct = await check_valid_number(phone_number)
        if not check_number_in_correct:
            return False
        query = select(self.model).where(self.model.phone_number == phone_number)
        promt = await self.session.execute(query)
        result = promt.scalars().one_or_none()
        if result is None:
            return True
        else:
            return False
