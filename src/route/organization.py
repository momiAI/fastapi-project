from fastapi import APIRouter, Body,HTTPException
from src.route.dependency import UserIdDep, DbDep, SerchNotBook
from src.schemas.organization import (
    OrganizationAdd,
    OrganizationUpdate
)
from src.utis.exception import IncorrectData,ObjectNotFound
from src.service.organization import OrganizationService


route = APIRouter(prefix="/organization", tags=["Организация"])


@route.get("/booked", summary="Свободные организации по дате")
async def not_booked(db: DbDep, data: SerchNotBook):
    result = await OrganizationService(db).not_booked(data)
    return {"message": "OK", "data": result}


@route.post("/add", summary="Регистрация организации")
async def add_organization(
    db: DbDep,
    user_id: UserIdDep,
    data: OrganizationAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Дворянская поляна",
                "value": {
                    "name": "Дворянская поляна",
                    "description": "Очень большое описание",
                    "city": "Донецк",
                    "location": "48.0000 37.0000",
                },
            }
        }
    ),
):
    
    return await OrganizationService(db).add_organization(user_id,data)


@route.delete("/delete/{id}", summary="Удаление организации")
async def delete_organization(db: DbDep, id: int):
    try:
        return await OrganizationService(db).delete_organization(id)
    except ObjectNotFound:
        return HTTPException(status_code=404, detail="Отель не найден")



@route.patch("/update/{id}", summary="Обновление организации")
async def update_organization(
    db: DbDep,
    id: int,
    data: OrganizationUpdate = Body(
        openapi_examples={
            "1": {
                "summary": "Обновление дворянской поляны",
                "value": {
                    "name": "Белая роща",
                    "description": "Ну очень большое описание",
                },
            }
        }
    ),
):
    try:
        result = await OrganizationService(db).update_organization(id,data)
        await db.commit()
        return result
    except IncorrectData:
        return HTTPException(status_code=400, detail="Некоректная дата отеля")

