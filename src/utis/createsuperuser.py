
from sqlalchemy import insert
from src.database import async_session_maker
from src.models.users import UsersModel
from src.schemas.users import UserIncludeId
from src.config import settings
from src.service.auth import authservice


async def create_super_user():
    data = UserIncludeId(
        email=settings.ADMIN_EMAIL,
        hash_password=authservice.hashed_password(settings.ADMIN_PASSWORD),
        last_name="Admin",
        first_name="Super",
        phone_number="+7777777777",
        role=2
    )
    async with async_session_maker() as session:
        stmt = insert(UsersModel).values(**data.model_dump())
        await session.execute(stmt)
        await session.commit()


