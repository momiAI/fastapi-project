from fastapi import APIRouter,Body,HTTPException,Query
from src.route.dependency import UserIdDep,DbDep, SerchNotBook
from src.schemas.cottage import CottageAdd,CottageUpdate

route = APIRouter(tags=["Котетджи"])

@route.get("/organization/{id_org}/cottage/{id_cott}", summary="Получение котетджа по айди")
async def get_cottage(db : DbDep,id_org : int,id_cott : int): 
        return await db.cottage.get_one_or_none(id = id_cott, organization_id = id_org)


@route.post("/organization/{id_org}/cottage/add", summary="Добавление коттеджа")
async def add_cottage(db : DbDep,id_org : int, data : CottageAdd = Body(openapi_examples={"1" : {"summary" : "Барский дом", "value" : {
    "name_house" : "Барский дом",
    "description" : "Огромный дом у речки на 8 человек",
    "people" : 8,
    "price" : 6000,
    "animals" : True
}
}})):
    data_update = data.model_dump()
    data_update.setdefault("organization_id", id_org)
    result = await db.cottage.insert_to_database(data_update)
    await db.commit()
    return {"message" : "OK", "data" : result } 
    

@route.patch("/organization/{id_org}/cottage/{id_cott}/update", summary = "Обновление коттеджа")
async def update_cottage(db : DbDep,id_org : int ,id_cott : int,id_user : UserIdDep, data : CottageUpdate = Body(openapi_examples={"1" : {"summary" : "Измененения 1", "value" : {
    "name_house" : "Императорский дом",
    "description" : "Ну очень огромный дом на 8 людишек",
    "price" : 10000
}}})):
    verify = await db.organization.get_access_user_by_org(id_org=id_org,id_user=id_user)
    if verify:
        result = await db.cottage.patch_object(id_cott,data.model_dump(exclude_unset=True))
        return {"message" : "OK", "data" : result}
    else: 
        return HTTPException(status_code=403, detail="Пользователь не имеет право на редактирование")
    

@route.get('/booked-cottage', summary= 'Получение свободных коттеджей по дате')
async def get_free_cottage(db : DbDep ,data : SerchNotBook, id_org : int | None = None):
     result = await db.cottage.get_free_cottage(id_org,data)
     return {'message' : 'OK' , 'data' : result} 