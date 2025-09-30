from fastapi import  Body, APIRouter,Depends
from src.schemas.house import HomePUT, HomePATCH 
from route.dependency import HomePagination
from src.database import async_session_maker
from src.models import HouseModel
from sqlalchemy import insert, values,select
from src.repositories.house import HouseRepository



route = APIRouter(prefix="/house", tags=["Дома"])







@route.get("/h",summary="Поиск с выборкой")
async def get_selection_homes(city: str | None = None,title : str | None = None, pag : HomePagination = Depends()):
    per_page = pag.per_page or 5 
    async with async_session_maker() as session: 
        return await HouseRepository(session).get_selection(city = city, title = title, page = pag.page, per_page = per_page)

            




@route.get("", summary="Вывод всех домов")
async def get_homes(pag : HomePagination = Depends()):
   per_page = pag.per_page or 5
   async with async_session_maker() as session:
        return await HouseRepository(session).get_all()

 


@route.delete("/{home_id}", summary="Удаление по айди" )
async def delete_home(home_id : int):
    for i in homes:
        if i["id"] == home_id:
            homes.remove(i)
    return {"status" : "OK", "homes" : homes}


@route.post("", summary="Добавление дома")
async def post_home(home_data : HomePUT = Body(openapi_examples={
    "1" : {"summary" : "Донецк", "value" : {
    "title" : "1-к Квартира бабушкин вариант",
    "city" : "Донецк",
    "street" : "Чижика",
    "number_house" : "2А",
    "square" : 38,
    "price" : 400000,
    "description" : "Продаётся там там та и т.д ",
    "number" : "+7-323-88-99-11",
    "rooms" : 1,
}}})):
    async with async_session_maker() as session:
        return await HouseRepository(session).insert_to_database(home_data.model_dump())
        

    


@route.put("/{home_id}", summary="Полное обновление дома")
async def put_home(home_id : int, home_data : HomePUT = Body(openapi_examples={
    "1" : {"summary" : "Донецк", "value" : {
    "city" : "Донецк",
    "street" : "Чижика",
    "number" : 27
}},
    "2" : {"summary" : "Торез", "value" : {
    "city" : "Торез",
    "street" : "Ульяновой",
    "number" : 12
}},

})
):
    for i in homes:
        if i["id"] == home_id and home_data.city != None and home_data.street != None and home_data.number != None:
            i["city"] = home_data.city
            i["street"] = home_data.street
            i["number"] = home_data.number

    return {"homes" : homes}


@route.patch("/{home_id}", summary="Частичное обновление дома")
async def patch_home(home_id : int, home_data : HomePATCH = Body(openapi_examples={
    "1" : {"summary" : "Без улицы", "value" : {
        "city" : "Торез",
        "number" : 33
    }
},
    "2" : {
    "summary" : "Без города", "value" : {
        "street" : "Чижика",
        "number" : 21
    }
}

})):
    for i in homes:
        if i["id"] == home_id:
            if home_data.city:
                i["city"] = home_data.city
            if home_data.street:
                i["street"] = home_data.street
            if home_data.number:
                i["number"] = home_data.number
    return {"homes" : homes}
