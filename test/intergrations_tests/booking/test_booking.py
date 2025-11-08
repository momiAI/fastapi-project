from datetime import date
from src.schemas.booking import Booking
from src.route.dependency import DateDep,HomePagination



async def test_get_all(db):
    await db.booking.get_all()


async def test_book_on_id_user(db):
    user_id = (await db.user.get_all())[0].id
    await db.booking.get_all_by_filter(user_id = user_id)


async def test_booked_cottage(db):
    id_org = (await db.organization.get_all())[0].id
    data = DateDep(date_start=date(2025,11,11) , 
                   date_end=date(2025,11,12))
    pag = HomePagination(page = 1, per_page=2)
    
    await db.booking.free_cottage(id_org,data,pag)