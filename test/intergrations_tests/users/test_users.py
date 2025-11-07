from src.schemas.users import UserAdd
from src.service.auth import authservice


async def test_login(db,ac):
    user = await db.user.get_one_or_none(email = "test@example.ru")
    access_token = authservice.create_access_token({
        "user_id" : user.id ,
        "user_role" : user.role
    })
    ac.cookies.set("access_token", access_token)

async def get_me(db):
    await db.user.get_one_or_none(id = 1)