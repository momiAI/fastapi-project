from fastapi import APIRouter,HTTPException
from src.route.dependency import UserIdDep, DbDep, UserRoleDep
from src.schemas.booking import BookingRequest



route = APIRouter(prefix="/booking", tags=["Бронирование"])

@route.get("/all", summary="Получение всех броней")
async def book_all(user_role : UserRoleDep, db : DbDep):
    if user_role != 1:
        return HTTPException(status_code=404, detail="Недостаточно прав")
    return await db.booking.get_all()


@route.get("/me", summary = "Получить бронирования пользователя")
async def book_me(user_id : UserIdDep, db : DbDep):
    return await db.booking.get_all_by_filter(user_id = user_id)


@route.post("/add",summary="Забронировать коттетдж")
async def book_cottage(user_id : UserIdDep, db : DbDep,data : BookingRequest):
    data_update = data.model_dump()
    cottage = await db.cottage.get_by_id(data_update.get("cottage_id"))
    data_update.update(price = cottage.price, user_id = user_id)
    result = await db.booking.insert_to_database(data_update)
    await db.commit()
    return {"message" : "OK","data" : result}

@route.get("/test")
async def testing(db : DbDep):
    result = await db.booking.test()
    return{"data" : result}