from src.schemas.house import HomeAdd,HomePATCH
from src.route.dependency import HomeSelection


async def test_house_add(db):
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
    await db.house.insert_to_database(data)
    await db.commit()


async def test_get_house(db):
    await db.house.get_by_id(1)


async def test_selection_home(db):
    data = HomeSelection(
        page = 1,
        per_page = 12,
        city = 'Донецк',
        title= None
    )
    await db.house.get_selection(data.model_dump(exclude_unset=True))


async def test_get_all(db):
    await db.house.get_all()




async def test_delete_home(db):
    id_house = (await db.house.get_all())[0].id
    await db.house.delete_by_id(id_house)


async def test_patch_home(db):
    data = HomePATCH(
        city = "Торез",
        number = '33',
        street  = None,
        number_house = None,
        square = None ,
        price = None,
        description = None,
        rooms= None
    )
    await db.house.patch_object(id = 1,data_patch = data)
    await db.commit()