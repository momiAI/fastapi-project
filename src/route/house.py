from fastapi import  Body, APIRouter,Depends
from src.schemas.house import HomeAdd, HomePATCH 
from route.dependency import HomeSelection, HomePagination
from src.route.dependency import DbDep
from fastapi_cache.decorator import cache


route = APIRouter(prefix="/house", tags=["Дома"])






@route.get("house/{id}",summary="Выбор объекта по айди")
async def get_house(id : int, db : DbDep):
    return await db.house.get_by_id(id)

@cache
@route.get("/h",summary="Поиск с выборкой")
async def get_selection_homes(db : DbDep,home_data : HomeSelection = Depends()):
    per_page = home_data.per_page or 5 
    return await db.house.get_selection(home_data.model_dump(exclude_unset=True))

            
@route.get("", summary="Вывод всех домов")
async def get_homes(db : DbDep,pag : HomePagination = Depends()):
   per_page = pag.per_page or 5
   return await db.house.get_all()

 
@route.delete("/delete/{id_house}", summary="Удаление по айди" )
async def delete_home(db : DbDep,id_house : int):
    result = await db.house.delete_by_id(id_house)
    await db.commit()
    return {"status" : "OK", "data" : result}


@route.post("/add", summary="Добавление дома")
async def post_home(db : DbDep,home_data : HomeAdd = Body(openapi_examples={
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
        result =  await db.house.insert_to_database(home_data)
        await db.commit()
        return {"status" : "OK", "data" : result}

    
@route.put("/edit", summary="Полное обновление дома")
async def put_home(db : DbDep,home_search : HomePATCH, home_data : HomeAdd = Body(openapi_examples={
    "1" : {"summary" : "Донецк", "value" : {
    "title" : "Квартира в центре города с хорошим ремонтом",
    "city" : "Донецк",
    "street" : "Чижика",
    "number_house" : "23Б",
    "square" : 52, 
    "description" : "Все вопросы по телефону",
    "number" : "+79296655331",
    "rooms" : 2
}},
    "2" : {"summary" : "Торез", "value" : {
    "title" : "Дом",
    "city" : "Торез",
    "street" : "Чижика",
    "number_house" : "2Б",
    "square" : 111, 
    "description" : "Обнов",
    "number" : "+79296655332",
    "rooms" : 13
}},

})
):
        result =  await db.house.edit_full(home_data,home_search)
        await db.commit()
        return {"status" : "OK", "data" : result}


@route.patch("/{home_id}", summary="Частичное обновление дома")
async def patch_home(db : DbDep,home_id : int, home_data : HomePATCH = Body(openapi_examples={
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
        result = await db.house.patch_object(home_id,home_data)
        await db.commit()
        return {"status" : "OK", "data" : result}
