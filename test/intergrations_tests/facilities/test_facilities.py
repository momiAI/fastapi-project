


async def test_get_all(ac):
    response = await ac.get("/facilitiec/cottage/all")
    assert response.status_code == 200


async def test_facilities_for_cottage_add(ac):
    response = await ac.post("/facilitiec/cottage/add",
                             json= {"title" : "Барбекю"}
                             )
    res = response.json()
    assert response.status_code == 200
    assert res["message"] == "OK"