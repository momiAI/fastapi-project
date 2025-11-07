from datetime import date 
from src.route.dependency import DateDep
from src.schemas.organization import OrganizationToDateBase,OrganizationUpdate




async def test_not_booked(db):
    data = DateDep(
        date_start=date(2025,11,7) ,
        date_end= date(2025,11,8)
    )
    await db.organization.get_free_organization_by_cottage(data)


async def test_delete_organization(db):
    id_org = (await db.organization.get_all())[0].id
    await db.organization.delete_by_id(id_org)


async def test_update_organization(db):
    id_org = (await db.organization.get_all())[0].id
    data = OrganizationUpdate(
        name  = "Белая роща",
        description  = "Огроменнные описание",
        city  = None,
        location  = None
    )

    await db.organization.patch_object(id_org,data)
    await db.commit()