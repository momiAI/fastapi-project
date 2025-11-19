from sqlalchemy import select,or_
from sqlalchemy.exc import NoResultFound,MultipleResultsFound

from .base import BaseRepository
from src.models.users import UsersModel
from src.repositories.utils import check_valid_number
from src.repositories.mappers.mappers import UserMapper
from src.utis.exception import TypeNumberError,KeyDuplication

class UserRepository(BaseRepository):
    model = UsersModel
    mapper = UserMapper

    async def check_number_and_email(self, phone_number, email):
        check_number_in_correct = await check_valid_number(phone_number)
        if not check_number_in_correct:
            raise TypeNumberError
        query = select(self.model).where(or_(self.model.phone_number == phone_number,self.model.email == email))
        promt = await self.session.execute(query)
        if promt.scalar() is None:
            return True
        else: 
            raise KeyDuplication
