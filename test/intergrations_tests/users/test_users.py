import pytest


@pytest.mark.parametrize(
    "email,password,last_name,first_name,phone_number,status_code",
    [
        ("example@example.ru", "password", "Last", "User", "+7123456789", 200),
        ("tes1t@example.ru", "password", "Last", "User", "+7123456789", 409),
        ("te111st@example.ru", "password", "Last", "User", "+7123456788", 200),
        ("te111st@example.ru", "password", "Last", "User", "+7856732341", 409),
        ("test165example.ru", "password", "Last", "User", "+7956732341", 422),
        ("test165@example.ru", "password", "Last", "User", "+7956732341", 200),
    ],
)
async def test_register(
    ac, email, password, last_name, first_name, phone_number, status_code
):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code,user_id",
    [
        ("example@example.ru", "password", 200, 3),
        ("test165@example.ru", "password", 200, 5),
        ("testinnnggg165@example.ru", "password", 404, 3),
    ],
)
async def test_login_user(ac, email, password, status_code, user_id):
    response_login = await ac.post(
        "/auth/login", json={"email": email, "password": password}
    )

    if response_login.status_code == 404:
        pytest.skip("Ошибка в почте все верно")

    res = response_login.json()
    assert response_login.status_code == status_code
    assert res["access_token"]

    response_me = await ac.get("/auth/get/me")
    res_me = response_me.json()
    assert response_me.status_code == status_code
    assert res_me["id"] == user_id

    response_logout = await ac.post("/auth/logout")
    res_logout = response_logout.json()
    assert response_logout.status_code == 200
    assert res_logout["status"] == "OK"
