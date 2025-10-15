from datetime import datetime
from sqlalchemy import delete,select,insert,values,func
from src.models.cottage import CottageModel
from src.models.booking import BookingModel
from src.database import async_session_maker
import asyncio


async def test():
    async with async_session_maker() as session:
        qeury1 = select(BookingModel.cottage_id, func.count().label('count')
                        ).where(BookingModel.date_start <= datetime(2025,11,10).date() , 
                         BookingModel.date_end >= datetime(2025,11,5).date()
                        ).group_by(BookingModel.id).cte("query1")
        qeury2 = select(CottageModel.id,
                        qeury1.c.count
                        ).outerjoin(qeury1, 
                        CottageModel.id == qeury1.c.cottage_id
                        ).cte("query2")
        
        qeury3 = select(qeury2).where(qeury2.c.count == None)
        print(qeury3.compile(compile_kwargs = {'literal_binds' : True})) 
        result = await session.execute(qeury3)
        print(result.keys())
        



asyncio.run(test())