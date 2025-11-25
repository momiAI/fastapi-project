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


async def booked_cottage(id_org: int | None, data: BaseModel, pag: BaseModel):
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
            .offset(per_page * (pag.page - 1))
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
            .offset(per_page * (pag.page - 1))
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


async def free_cottage(id_org: int | None, data: BaseModel, pag : BaseModel):
    per_page = 5 or pag.per_page
    cte = (
        select(b.id,c.id.label("cottage_id"),c.price,b.date_start,b.date_end,c.organization_id)
    .outerjoin(c,b.cottage_id == c.id)
    .where(b.date_end >= data.date_start, b.date_start <= data.date_end)
    .cte("booked_cottage")
    )
    if id_org is None:
        query = (select(c).outerjoin(cte,c.id == cte.c.cottage_id)
                 .where(cte.c.date_start == None) # noqa: E711
                 .offset(per_page * (pag.page - 1)).limit(per_page))
    else:
        query = (select(c).outerjoin(cte,c.id == cte.c.cottage_id)
                 .where(cte.c.date_start == None,c.organization_id == id_org) # noqa: E711
                 .offset(per_page * (pag.page - 1)).limit(per_page))
    return query

def upload_image(name, image, id_cott):
    path = f"src/static/img/{str(id_cott) + name}"
    with open(path, "wb+") as new_file:
        shutil.copyfileobj(image, new_file)
    return path
