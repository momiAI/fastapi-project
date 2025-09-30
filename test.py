from sqlalchemy import delete,select,insert,values
from src.models import HouseModel
from src.database import async_session_maker
import asyncio


async def test():
    async with async_session_maker() as session:
        qeury = select(HouseModel.title, HouseModel.city).where(HouseModel.title.ilike("%Дом%"))
        print(qeury.compile(compile_kwargs = {'literal_binds' : True})) 
        result = await session.execute(qeury)
        print(result.scalars().all())



asyncio.run(test())