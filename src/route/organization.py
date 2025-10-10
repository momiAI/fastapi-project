from fastapi import APIRouter,Body
from src.route.dependency import UserIdDep,DbDep
from src.schemas.organization import OrganizationAdd, OrganizationUpdate




route = APIRouter(prefix="/organization", tags=["Организация"])

@route.post("/add", summary="Регистрация организации")
async def add_organization(db : DbDep, user_id : UserIdDep,data : OrganizationAdd = Body(openapi_examples = {"1" : {"summary" : "Дворянская поляна", "value" : {
    "name" : "Дворянская поляна",
    "description" : "Очень большое описание",
    "city" : "Донецк",
    "location" : "48.0000 37.0000"
}}} )):
    update_data = data.model_dump()
    update_data.setdefault("user_id", user_id)
    result = await db.organization.insert_to_database(update_data)
    await db.commit()
    return result


@route.delete("/delete/{id}", summary="Удаление организации")
async def delete_organization(db : DbDep, id : int):
        result = await db.organization.delete_by_id(id)
        await db.commit()
        return result


@route.patch("/update/{id}", summary="Обновление организации")
async def update_organization(db : DbDep, id : int, data : OrganizationUpdate = Body(openapi_examples={"1" : {"summary" : "Обновление дворянской поляны","value" : {
    "name" : "Белая роща",
    "description" : "Ну очень большое описание"
}}})):
        result = await db.organization.patch_object(id,data.model_dump(exclude_unset= True))
        await db.commit()
        return result