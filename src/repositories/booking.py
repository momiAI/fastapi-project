from pydantic import BaseModel
from sqlalchemy import delete
from datetime import date

from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.repositories.utils import booked_cottage, booked_cottages
from src.repositories.mappers.mappers import BookingMapper


class BookingRepository(BaseRepository):
    model = BookingModel
    mapper = BookingMapper

    async def free_cottage(self, id_org: int, data: BaseModel, pag: BaseModel):
        query = await booked_cottage(id_org, data, pag)
        return await self.get_filtered(BookingModel.cottage_id.in_(query))

    async def booked_cottage_or_no(
        self, id_cott: int, date_start: date, date_end: date
    ):
        query = await booked_cottages(
            id_cott=id_cott, date_start=date_start, date_end=date_end
        )
        result = await self.session.execute(query)
        if result.scalars().all() == []:
            return True
        else:
            return False

    async def delete_from_test(self):
        await self.session.execute(delete(self.model))
