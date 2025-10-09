from fastapi import APIRouter,Body
from src.database import async_session_maker
from src.repositories.cottage import CottageRepository
from src.schemas.cottage import CottageAdd

route = APIRouter(prefix="organization/{id_org}/cottage", tags=["Котетджи"])

@route.get("/{id}", summary="Получение котетджа по айди")
async def get_cottage(id : int): 
    async with async_session_maker() as session:
        return await CottageRepository(session).get_one_or_none(id = id)


@route.post("/add", summary="Добавление коттеджа")
async def add_cottage(id_org : int, data : CottageAdd = Body(openapi_examples={"1" : {"summary" : "Барский дом", "value" : {
    "name_house" : "Барский дом",
    "description" : "Огромный дом у речки на 8 человек",
    "people" : 8,
    "price" : 6000,
    "animals" : True
}
}})):
    data_update = data.model_dump()
    data_update.setdefault("organization_id", id_org)
    async with async_session_maker() as session: 
        result = await CottageRepository(session).insert_to_database(data_update)
        await session.commit()
        return {"message" : "OK", "data" : result } 
    

        