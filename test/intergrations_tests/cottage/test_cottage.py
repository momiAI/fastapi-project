from datetime import date
from src.route.dependency import HomePagination,DateDep
from src.schemas.cottage import CottageAdd,CottageToDateBase,CottageUpdateToDateBase
from src.schemas.facilities import AsociationFacilitiesCottage


async def test_get(db): 

    await db.cottage.get_one_or_none(id = 1, organization_id = 1)


async def test_get_free_cottge(db):

    id_org = (await db.organization.get_all())[0].id
    date_data = DateDep(date_start=date(2025,11,7) , date_end=date(2025,11,8) )
    pag = HomePagination(page = 1, per_page=2)

    await db.cottage.get_free_cottage(id_org,date_data,pag)


async def update_cottage(db):
    id_cott = (await db.cottage.get_all())[0].id
    cottage = CottageUpdateToDateBase(
        name_house = "Императорский дом",
        description = "Ну очень огромный дом на 8 людишек",
        price = 10000,
    )
    await db.cottage.patch_object(id_cott,cottage)
    await db.asociatfacilcott.patch_facilities(id_cott,[1,2,3])
    await db.session.commit()