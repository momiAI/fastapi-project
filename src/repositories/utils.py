import shutil
from pydantic import BaseModel
from sqlalchemy import select,func,insert
from src.models.booking import BookingModel as b
from src.models.cottage import CottageModel as c
from src.models.images import ImagesModel as img
from src.models.organization import OrganizationModel as o



async def booked_cottage(id_org : int,data : BaseModel, pag : BaseModel):
        per_page = 5 or pag.per_page
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
                                                                      c.id.in_(select(c.id).where(c.organization_id == id_org))).offset(pag.page).limit(per_page)
        else: 
            query = select(c.id).outerjoin(booked_cottage, c.id == booked_cottage.c.id
                                                              ).where(func.coalesce(booked_cottage.c.cottage_count,0) == 0, 
                                                                      c.id.in_(select(c.id))).offset(pag.page * (per_page - 1)).limit(per_page)
        return query

async def booked_organization(data : BaseModel):
     booked_cottage =  select(c.id,
                                c.price,
                                func.count('*').label('cottage_count')
                                ).join(b).where( 
                                     
                                    b.date_end >= data.date_start,
                                    b.date_start <= data.date_end
                                ).group_by(c.id).cte('booked_cottage')
     
     query = select(o.id).select_from(c).outerjoin(booked_cottage, c.id == booked_cottage.c.id
                                                              ).join(o, c.organization_id == o.id).where(func.coalesce(booked_cottage.c.cottage_count,0) == 0, 
                                                                      c.id.in_(select(c.id))
                                                                      ).group_by(o.id)
     return query


def upload_image(name,image,id_cott):
    path = f'src/static/img/{str(id_cott) + name}'
    with open(path,"wb+") as new_file:
        shutil.copyfileobj(image, new_file)
    return path