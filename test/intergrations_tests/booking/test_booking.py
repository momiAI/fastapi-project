from datetime import date
from src.schemas.booking import Booking
from src.route.dependency import DateDep,HomePagination



async def test_get_all(test_auth_user_ac):
    response = await test_auth_user_ac.get("/booking/all")
    assert response.status_code == 200


async def test_book_me(test_auth_user_ac):
    response = await test_auth_user_ac.get("/booking/me")
    assert response.status_code == 200


async def test_book_cottage(db,test_auth_user_ac):
    cottage_id = (await db.cottage.get_all())[0].id
    response = await test_auth_user_ac.post("/booking/add", json = {
        "cottage_id" : cottage_id,
        "date_start" : "2025-11-07",
        "date_end" : "2025-11-08"
    })
    res = response.json()
    assert res["message"] == 'OK' 



async def test_booked_cottage(test_auth_user_ac):
    response = await test_auth_user_ac.get("/booking/booked", params = {
        "date_start" : "2025-11-07",
        "date_end" : "2025-11-08"
    })
    
    assert response.status_code == 200