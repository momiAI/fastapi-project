from fastapi import APIRouter, HTTPException, Depends
from src.route.dependency import UserIdDep, DbDep, UserRoleDep, SerchNotBook
from src.schemas.booking import BookingRequest
from src.route.dependency import HomePagination
from src.utis.exception import CottageBook, CottageNotFound,AccessDenied
from src.service.booking import BookingService

route = APIRouter(prefix="/booking", tags=["Бронирование"])


@route.get("/all", summary="Получение всех броней")
async def book_all(user_role: UserRoleDep, db: DbDep):
    try:
        return await BookingService(db).book_all(user_role)
    except AccessDenied as ex:
        raise HTTPException(status_code=403, detail=ex.detail)


@route.get("/me", summary="Получить бронирования пользователя")
async def book_me(user_id: UserIdDep, db: DbDep):
    return await BookingService(db).book_me(user_id)


@route.post("/add", summary="Забронировать коттетдж")
async def book_cottage(user_id: UserIdDep, db: DbDep, data: BookingRequest):
    try:
        result = await BookingService(db).book_cottage(user_id,data)
    except CottageNotFound as ex:
        raise HTTPException(status_code=404, detail=ex.detail)
    except CottageBook as ex:
        raise HTTPException(status_code=409, detail=ex.detail)

    return {"message": "OK", "data": result}


@route.get("/booked")
async def booked_cottage(
    db: DbDep,
    date: SerchNotBook,
    id_org: int | None = None,
    pag: HomePagination = Depends(),
):
    result = await BookingService(db).booked_cottage(date,id_org, pag)
    return {"data": result}
