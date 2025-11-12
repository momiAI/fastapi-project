import pytest
from src.schemas.users import UserAdd
from src.service.auth import authservice


@pytest.mark.parametrize("email,password,last_name,first_name,phone_number,status_code",[
    ("test@example.ru","password","Last","User","+7856732341", 200),
    ("tes1t@example.ru","password","Last","User","+7856732341", 400),
    ("te111st@example.ru","password","Last","User","+7856732341", 400),
    ("test1@example.ru","password","Last","User","+7856732341", 400),
    ("te1st@example.ru","password","Last","User","+7856732341", 400),
    ("test165example.ru","password","Last","User","+7956732341", 422),
    ("test165@example.ru","password","Last","User","+7956732341", 200)
]
)
async def test_register(ac,
                        email,
                        password,
                        last_name,
                        first_name,
                        phone_number,
                        status_code):
    response = await ac.post("/auth/register" , json= {
        "email" : email,
        "password" : password,
        "first_name" : first_name,
        "last_name" : last_name,
        "phone_number" : phone_number
    })
    assert response.status_code == status_code



async def get_me(ac):
    response = await ac.get("/auth/get/me")
    assert response.status_code == 200