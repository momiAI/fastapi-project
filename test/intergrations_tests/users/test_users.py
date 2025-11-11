from src.schemas.users import UserAdd
from src.service.auth import authservice


async def get_me(ac):
    response = await ac.get("/auth/get/me")
    assert response.status_code == 200