from fastapi import APIRouter, HTTPException, Depends
from src.route.dependency import UserIdDep, DbDep, UserRoleDep, SerchNotBook
from src.schemas.booking import BookingRequest, Booking
from src.route.dependency import HomePagination
from src.utis.exception import ObjectNotFound


route = APIRouter(prefix="/booking", tags=["Бронирование"])


@route.get("/all", summary="Получение всех броней")
async def book_all(user_role: UserRoleDep, db: DbDep):
    if user_role != 1:
        return HTTPException(status_code=403, detail="Недостаточно прав")
    return await db.booking.get_all()


@route.get("/me", summary="Получить бронирования пользователя")
async def book_me(user_id: UserIdDep, db: DbDep):
    return await db.booking.get_all_by_filter(user_id=user_id)


@route.post("/add", summary="Забронировать коттетдж")
async def book_cottage(user_id: UserIdDep, db: DbDep, data: BookingRequest):
    if data.date_start > data.date_end:
        raise HTTPException(status_code=400, detail="Проверьте дату бронирования.")
    try:
        cottage = await db.cottage.get_by_id(data.cottage_id)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Коттетдж не найден")
    check = await db.booking.booked_cottage_or_no(
        data.cottage_id, data.date_start, data.date_end
    )
    if not check:
        raise HTTPException(status_code=401, detail="Котетдж забронирован")
    data_update = Booking(price=cottage.price, user_id=user_id, **data.model_dump())
    result = await db.booking.insert_to_database(data_update)
    await db.commit()
    return {"message": "OK", "data": result}


@route.get("/booked")
async def booked_cottage(
    db: DbDep,
    date: SerchNotBook,
    id_org: int | None = None,
    pag: HomePagination = Depends(),
):
    result = await db.booking.free_cottage(id_org, date, pag)
    return {"data": result}
