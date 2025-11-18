from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from .base import BaseRepository
from src.models.users import UsersModel
from src.repositories.utils import check_valid_number
from src.repositories.mappers.mappers import UserMapper
from src.utis.exception import TypeNumberError,KeyDuplication

class UserRepository(BaseRepository):
    model = UsersModel
    mapper = UserMapper

    async def check_number(self, phone_number):
        check_number_in_correct = await check_valid_number(phone_number)
        if not check_number_in_correct:
            raise TypeNumberError
        query = select(self.model).where(self.model.phone_number == phone_number)
        promt = await self.session.execute(query)
        try:
            promt.scalar_one()
        except NoResultFound:
            raise KeyDuplication