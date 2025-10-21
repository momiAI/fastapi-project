from pydantic import BaseModel
from sqlalchemy import select,func
from src.models.booking import BookingModel as b
from src.models.cottage import CottageModel as c



async def booked_cottage(id_org : int,data : BaseModel):
        booked_cottage = select(c.id,
                                c.price,
                                func.count('*').label('cottage_count')
                                ).join(b).where( 
                                    b.date_end >= data.date_start,
                                    b.date_start <= data.date_end
                                ).group_by(c.id).cte('booked_cottage')
        if id_org is not None:
            query = select(c.id).outerjoin(booked_cottage, c.id == booked_cottage.c.id
                                                              ).where(func.coalesce(booked_cottage.c.cottage_count,0) == 0, 
                                                                      c.id.in_(select(c.id).where(c.organization_id == id_org)))
        else: 
            query = select(c.id).outerjoin(booked_cottage, c.id == booked_cottage.c.id
                                                              ).where(func.coalesce(booked_cottage.c.cottage_count,0) == 0, 
                                                                      c.id.in_(select(c.id)))
        return query

async def booked_organization(data : BaseModel):
     booked_cottage =  select(c.id,
                                c.price,
                                func.count('*').label('cottage_count')
                                ).join(b).where( 
                                    b.date_end >= data.date_start,
                                    b.date_start <= data.date_end
                                ).group_by(c.id).cte('booked_cottage')
     
     query = select(c.id).outerjoin(booked_cottage, c.id == booked_cottage.c.id
                                                              ).where(func.coalesce(booked_cottage.c.cottage_count,0) == 0, 
                                                                      c.id.in_(select(c.id)))
    # Дописать функцию для организаци !!!!!