from fastapi import APIRouter,Body
from src.database import async_session_maker
from src.route.dependency import UserIdDep
from src.repositories.organization import OrganizationRepository
from src.schemas.organization import OrganizationAdd, OrganizationUpdate




route = APIRouter(prefix="/organization", tags=["Организация"])

@route.post("/add", summary="Регистрация организации")
async def add_organization(user_id : UserIdDep,data : OrganizationAdd = Body(openapi_examples = {"1" : {"summary" : "Дворянская поляна", "value" : {
    "name" : "Дворянская поляна",
    "description" : "Очень большое описание",
    "city" : "Донецк",
    "location" : "48.0000 37.0000"
}}} )):
    update_data = data.model_dump()
    update_data.setdefault("user_id", user_id)
    print(update_data)
    async with async_session_maker() as session: 
        result = await OrganizationRepository(session).insert_to_database(update_data)
        await session.commit()
        return result


@route.delete("/delete/{id}", summary="Удаление организации")
async def delete_organization(id : int):
    async with async_session_maker() as session: 
        result = await OrganizationRepository(session).delete_by_id(id)
        await session.commit()
        return result


@route.patch("/update/{id}", summary="Обновление организации")
async def update_organization(id : int, data : OrganizationUpdate = Body(openapi_examples={"1" : {"summary" : "Обновление дворянской поляны","value" : {
    "name" : "Белая роща",
    "description" : "Ну очень большое описание"
}}})):
    async with async_session_maker() as session: 
        result = await OrganizationRepository(session).patch_object(id,data.model_dump(exclude_unset= True))
        await session.commit()
        return result