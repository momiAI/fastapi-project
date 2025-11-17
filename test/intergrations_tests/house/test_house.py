async def test_get_by_id(ac):
    response = await ac.get("/house/by/1")
    assert response.status_code == 200


async def test_get_by_selection(ac):
    response = await ac.get("/house/selection", params={"city": "Донецк"})
    assert response.status_code == 200


async def test_get_all(ac):
    response = await ac.get("/house/all")
    assert response.status_code == 200


async def test_house_add(ac):
    response = await ac.post(
        "/house/add",
        json={
            "title": "1-к Квартира бабушкин вариант",
            "city": "Донецк",
            "street": "Чижика",
            "number_house": "2А",
            "square": 38,
            "price": 400000,
            "description": "Продаётся там там та и т.д ",
            "number": "+7-323-88-99-11",
            "rooms": 1,
        },
    )
    assert response.status_code == 200


async def test_patch_home(ac, db):
    id_house = (await db.house.get_all())[0].id
    response = await ac.patch(
        f"/house/patch/{id_house}", json={"city": "Торез", "number": "33"}
    )
    assert response.status_code == 200


async def test_delete_by_id(ac):
    response = await ac.delete("/house/delete/1")
    assert response.status_code == 200
