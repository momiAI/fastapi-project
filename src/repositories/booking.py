from datetime import datetime
from sqlalchemy import select,insert,values,update,or_,delete,func
from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.models.cottage import CottageModel
from src.schemas.booking import Booking


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = Booking

    async def test(self):
        query1 = select(self.model.cottage_id,func.count()).where(self.model.date_start <= datetime(2025,11,21).date()).group_by(self.model.cottage_id).cte("cottage_book")
        query2 = select(CottageModel.id, query1.columns.count).outerjoin(query1,CottageModel.id == query1.c.cottage_id).cte("cottage1")
        
        #query3 = select(query2).where(query2.c.count == 0)
        print(query2.compile(compile_kwargs = {"literal_binds" : True}))

        return query2