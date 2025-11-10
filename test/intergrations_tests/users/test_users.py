from src.schemas.users import UserAdd
from src.service.auth import authservice


async def get_me(db):
    await db.user.get_one_or_none(id = 1)