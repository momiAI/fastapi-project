from datetime import date
from src.route.dependency import HomePagination,DateDep
from src.schemas.cottage import CottageAdd,CottageToDateBase,CottageUpdateToDateBase
from src.schemas.facilities import AsociationFacilitiesCottage


async def test_get(ac,db): 
    response = await ac.get("/organization/1/cottage/1")
    assert response.status_code == 200


async def test_get_free_cottge(ac):
    response = await ac.get("/booked-cottage", params= {
        "date_start" : "2025-11-07",
        "date_end" : "2025-11-08"
    })

    assert response.status_code == 200


async def test_add_cottage(ac,db):
    organization_id = (await db.organization.get_all())[0].id
    response = await ac.post(f"/organization/{organization_id}/cottage/add", 
        params = {
            "organization_id" : int(organization_id)
        },
        json = {
            "name_house" : "Ванькин дом",
            "description" : "Большой дом",
            "people" : 8,
            "price" : 8000,
            "facilities_ids" : (4,5,6)
    })
    res = response.json()
    assert res["message"] == "OK"


async def test_update_cottage(db,test_auth_user_ac,test_add_cottage,test_add_facilitie_cottage):
    id_cott = (await db.cottage.get_all())[0].id
    response = await test_auth_user_ac.patch(
        f"/organization/1/cottage/{id_cott}/update",
        json = {
            "name_house" : "Императорский дом",
            "description" : "Ну очень огромный дом на 8 людишек",
            "price" : 10000,
            "facilities_ids" : [3,4,5]
        }
    )
    res = response.json()
    assert res["message"] == "OK"
