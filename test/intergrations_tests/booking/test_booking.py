from datetime import date
from src.schemas.booking import Booking
from src.route.dependency import DateDep



async def test_book_cottage(db):
    cottage_id = (await db.cottage.get_all())[0].id
    user_id = (await db.user.get_all())[0].id

    data = Booking(
        cottage_id= cottage_id,
        user_id=user_id,
        date_start = date(2025,11,11),
        date_end = date(2025,11,12),
        price = 6000
    )

    await db.booking.insert_to_database(data)
    await db.commit()


async def test_get_all(db):
    await db.booking.get_all()


async def test_book_on_id_user(db):
    user_id = (await db.user.get_all())[0].id
    await db.booking.get_all_by_filter(user_id = user_id)


async def test_booked_cottage(db):
    id_org = (await db.organization.get_all())[0].id
    data = DateDep(date_start=date(2025,11,11) , 
                   date_end=date(2025,11,12))

    await db.booking.free_cottage(id_org,data)