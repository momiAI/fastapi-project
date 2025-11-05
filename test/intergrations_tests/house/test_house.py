from src.schemas.house import HomeAdd
from src.database import async_session_maker
from src.utis.db_manager import DbManager


async def test_house_add():
    data = HomeAdd(
        title = "1-к Квартира бабушкин вариант",
        city = "Донецк",
        street = "Чижика",
        number_house = "2А",
        square = 38,
        price = 400000,
        description = "Продаётся там там та и т.д" ,
        number = "+7-323-88-99-11",
        rooms = 1
    )
    async with DbManager(session_factory=async_session_maker) as db:
        result = await db.house.insert_to_database(data)
        await db.commit()

