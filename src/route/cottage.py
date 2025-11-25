from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, HTTPException, Depends, UploadFile
from src.route.dependency import UserIdDep, DbDep, SerchNotBook, HomePagination
from src.schemas.cottage import (
    CottageAdd,
    CottageUpdate
)
from src.utis.exception import FacilitiesNotFound,IncorrectDataCottage,CottageNotFound, OrganizationNotFound, UserHasNotPermission
from src.service.cottage import CottageService

route = APIRouter(tags=["Котетджи"])


@route.get(
    "/organization/{id_org}/cottage/{id_cott}", summary="Получение котетджа по айди"
)
async def get_cottage(db: DbDep, id_org: int, id_cott: int):
    try:
        return await CottageService(db).get_cottage(id_org,id_cott)
    except CottageNotFound:        
        raise HTTPException(status_code=400, detail="Котетдж не найден")


@cache(expire=20)
@route.get("/booked-cottage", summary="Получение свободных коттеджей по дате")
async def get_free_cottage(
    db: DbDep,
    data: SerchNotBook,
    pag: HomePagination = Depends(),
    id_org: int | None = None,
):
    result = await CottageService(db).get_free_cottage(data,pag,id_org)
    if result == []:
        raise HTTPException(status_code=404, detail="Свободных отелей на данную дату нет.")
    return {"message": "OK", "data": result}


@route.post("/organization/{id_org}/cottage/add", summary="Добавление коттеджа")
async def add_cottage(
    db: DbDep,
    user : UserIdDep,
    id_org: int,
    data: CottageAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Барский дом",
                "value": {
                    "name_house": "Барский дом",
                    "description": "Огромный дом у речки на 8 человек",
                    "people": 8,
                    "price": 6000,
                    "animals": True,
                    "facilities_ids": [4, 7, 8],
                },
            }
        }
    ),
):  
    try:
        cottage = await CottageService(db).add_cottage(id_org,data)
    except OrganizationNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    except IncorrectDataCottage as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    except FacilitiesNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
        
    return {"message": "OK", "data": cottage}


@route.patch(
    "/organization/{id_org}/cottage/{id_cott}/update", summary="Обновление коттеджа"
)
async def update_cottage(
    db: DbDep,
    id_org: int,
    id_cott: int,
    id_user: UserIdDep,
    data: CottageUpdate = Body(
        openapi_examples={
            "1": {
                "summary": "Измененения 1",
                "value": {
                    "name_house": "Императорский дом",
                    "description": "Ну очень огромный дом на 8 людишек",
                    "price": 10000,
                    "facilities_ids": [5, 6, 9],
                },
            }
        }
    ),
):
    try:
        cottage = await CottageService(db).update_cottage(id_org,id_cott,id_user,data)
    except UserHasNotPermission as ex:
        raise HTTPException(status_code=403, detail=ex.detail)
    except IncorrectDataCottage as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    except CottageNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    except FacilitiesNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.detail)

    return {"message": "OK", "data": cottage}


@route.post("/cottage/{id_cott}/add-img", summary="Добавления картинки к котетджу")
async def add_img_cottage(db: DbDep, id_cott: int, images: UploadFile):
    await CottageService(db).add_img_cottage(id_cott,images)
    return {"message": "OK"}
