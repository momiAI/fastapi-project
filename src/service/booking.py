

import logging
from src.route.dependency import SerchNotBook, UserIdDep, UserRoleDep
from src.schemas.booking import Booking, BookingRequest
from src.service.base import BaseService
from src.utis.exception import AccessDenied, ObjectNotFound,CottageNotFound,CottageBook


class BookingService(BaseService):

    async def book_all(self,user_role: UserRoleDep):
        if user_role != 1:
            return AccessDenied
        return await self.db.booking.get_all()


    async def book_me(self,user_id: UserIdDep):
        return await self.db.booking.get_all_by_filter(user_id=user_id)



    async def book_cottage(self,user_id: UserIdDep,data: BookingRequest):
        try:
            cottage = await self.db.cottage.get_by_id(data.cottage_id)
        except ObjectNotFound:
            logging.debug(f"Не удалось найти коттедж с id : {data.cottage_id}")
            raise CottageNotFound
        check = await self.db.booking.booked_cottage_or_no(
            data.cottage_id, data.date_start, data.date_end
        )
        if not check:
            raise CottageBook
        data_update = Booking(price=cottage.price, user_id=user_id, **data.model_dump())
        result = await self.db.booking.insert_to_database(data_update)
        await self.db.commit()
        return {"message": "OK", "data": result}


    async def booked_cottage(
        date: SerchNotBook,
        id_org: int | None = None,
        pag: HomePagination = Depends(),
    ):
        result = await db.booking.free_cottage(id_org, date, pag)
        return {"data": result}
