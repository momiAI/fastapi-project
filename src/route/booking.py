from fastapi import APIRouter
from src.route.dependency import UserIdDep, DbDep
from src.schemas.booking import BookingRequest



route = APIRouter(prefix="/booking", tags=["Бронирование"])


@route.post("/add",summary="Забронировать коттетдж")
async def book_cottage(user_id : UserIdDep, db : DbDep,data : BookingRequest):
    data_update = data.model_dump()
    cottage = await db.cottage.get_by_id(data_update.get("cottage_id"))
    data_update.update(price = cottage.price, user_id = user_id)
    result = await db.booking.insert_to_database(data_update)
    await db.commit()
    return {"message" : "OK","data" : result}