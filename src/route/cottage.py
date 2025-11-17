from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, HTTPException, Depends, UploadFile
from src.route.dependency import UserIdDep, DbDep, SerchNotBook, HomePagination
from src.schemas.cottage import (
    CottageAdd,
    CottageUpdate,
    CottageToDateBase,
    CottageUpdateToDateBase,
)
from src.schemas.facilities import AsociationFacilitiesCottage
from src.schemas.images import ImageAdd, AsociationImagesCottage
from src.repositories.utils import upload_image
from src.tasks.tasks_storage import resize_image


route = APIRouter(tags=["Котетджи"])


@route.get(
    "/organization/{id_org}/cottage/{id_cott}", summary="Получение котетджа по айди"
)
async def get_cottage(db: DbDep, id_org: int, id_cott: int):
    return await db.cottage.get_one_or_none(id=id_cott, organization_id=id_org)


@cache(expire=20)
@route.get("/booked-cottage", summary="Получение свободных коттеджей по дате")
async def get_free_cottage(
    db: DbDep,
    data: SerchNotBook,
    pag: HomePagination = Depends(),
    id_org: int | None = None,
):
    result = await db.cottage.get_free_cottage(id_org, data, pag)
    return {"message": "OK", "data": result}


@route.post("/organization/{id_org}/cottage/add", summary="Добавление коттеджа")
async def add_cottage(
    db: DbDep,
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
    data_update = CottageToDateBase(organization_id=id_org, **data.model_dump())
    cottage = await db.cottage.insert_to_database(data_update)
    await db.asociatfacilcott.insert_to_database_bulk(
        [
            AsociationFacilitiesCottage(id_cottage=cottage.id, id_facilities=i)
            for i in data.facilities_ids
        ]
    )
    await db.commit()
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
    verify = await db.organization.get_access_user_by_org(
        id_org=id_org, id_user=id_user
    )
    if not verify:
        return HTTPException(
            status_code=403, detail="Пользователь не имеет право на редактирование"
        )
    cottage = await db.cottage.patch_object(
        id_cott, CottageUpdateToDateBase(**data.model_dump(exclude_unset=True))
    )
    if data.facilities_ids:
        await db.asociatfacilcott.patch_facilities(id_cott, data.facilities_ids)

    await db.session.commit()

    return {"message": "OK", "data": cottage}


@route.post("/cottage/{id_cott}/add-img", summary="Добавления картинки к котетджу")
async def add_img_cottage(db: DbDep, id_cott: int, images: UploadFile):
    img_stmt = await db.images.insert_to_database(
        ImageAdd(name_img=str(id_cott) + str(images.filename))
    )
    await db.asociatimagecottage.insert_to_database(
        AsociationImagesCottage(id_img=img_stmt.id, id_cottage=id_cott)
    )
    path = upload_image(images.filename, images.file, id_cott)
    resize_image.delay(path)
    await db.session.commit()
    return {"message": "OK"}
