import shutil
from pydantic import BaseModel
from datetime import date
from sqlalchemy import select, func

from src.models.booking import BookingModel as b
from src.models.cottage import CottageModel as c
from src.models.organization import OrganizationModel as o


async def booked_cottages(id_cott: int, date_start: date, date_end: date):
    query = select(b.cottage_id).where(
        b.cottage_id == id_cott, b.date_end >= date_start, b.date_start <= date_end
    )
    return query


async def check_valid_number(phone_number: str):
    if (
        phone_number[0] == "+"
        and len(phone_number) == 11
        and (phone_number[1] == "7" or phone_number[1] == "8")
    ):
        return True
    else:
        False


async def booked_cottage(id_org: int, data: BaseModel, pag: BaseModel):
    per_page = 5 or pag.per_page
    booked_cottage = (
        select(c.id, c.price, func.count("*").label("cottage_count"))
        .join(b)
        .where(b.date_end >= data.date_start, b.date_start <= data.date_end)
        .group_by(c.id)
        .cte("booked_cottage")
    )
    if id_org is not None:
        query = (
            select(c.id)
            .outerjoin(booked_cottage, c.id == booked_cottage.c.id)
            .where(
                func.coalesce(booked_cottage.c.cottage_count, 0) == 0,
                c.id.in_(select(c.id).where(c.organization_id == id_org)),
            )
            .offset(pag.page)
            .limit(per_page)
        )
    else:
        query = (
            select(c.id)
            .outerjoin(booked_cottage, c.id == booked_cottage.c.id)
            .where(
                func.coalesce(booked_cottage.c.cottage_count, 0) == 0,
                c.id.in_(select(c.id)),
            )
            .offset(pag.page * (per_page - 1))
            .limit(per_page)
        )
    return query


async def booked_organization(data: BaseModel):
    booked_cottage = (
        select(c.id, c.price, func.count("*").label("cottage_count"))
        .join(b)
        .where(b.date_end >= data.date_start, b.date_start <= data.date_end)
        .group_by(c.id)
        .cte("booked_cottage")
    )

    query = (
        select(o.id)
        .select_from(c)
        .outerjoin(booked_cottage, c.id == booked_cottage.c.id)
        .join(o, c.organization_id == o.id)
        .where(
            func.coalesce(booked_cottage.c.cottage_count, 0) == 0,
            c.id.in_(select(c.id)),
        )
        .group_by(o.id)
    )
    return query
'''with booked_cottage as (
	select 
		  b.id,
	      c.id as cottage_id,
	      c.price,
	      b.date_start,
	      b.date_end  
	from 
		booking b
	right join 
		cottage c 
	on 
	b.cottage_id = c.id
	where b.date_start <=  '2025-11-11' and  b.date_end >=  '2025-11-09'
)
select bc.cottage_id 
from 
	cottage c 
left join booked_cottage bc on bc.cottage_id = c.id
where c.price = Null'''

async def free_cottage(id_org: int | None, data: BaseModel):
    query = (
        select(b.id,c.id.label("cottage_id"),c.price,b.date_start,b.date_end)
    .outerjoin(c,b.cottage_id == c.id)
    .where(b.date_end >= data.date_start, b.date_start <= data.date_end)
    .cte("booked_cottage")
    )
    return query

def upload_image(name, image, id_cott):
    path = f"src/static/img/{str(id_cott) + name}"
    with open(path, "wb+") as new_file:
        shutil.copyfileobj(image, new_file)
    return path
