from datetime import datetime,date
from pydantic import BaseModel
from sqlalchemy import select,insert,values,update,or_,delete,func
from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.models.cottage import CottageModel
from src.schemas.booking import Booking


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = Booking

    async def booked(self, data : BaseModel):
        query1 = select(self.model.cottage_id,func.count().label("count")
                        ).where(self.model.date_start <= data.date_end , self.model.date_end >= data.date_start
                                ).group_by(self.model.cottage_id).cte("query1")
        query2 = select(CottageModel.id, query1.columns.count).outerjoin(query1,CottageModel.id == query1.c.cottage_id).cte("query2")
        query3 = select(query2).where(query2.c.count == None)
        result = await self.session.execute(query3)

        return result.scalars().all()