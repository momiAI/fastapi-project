from sqlalchemy import select 
from sqlalchemy.orm import selectinload,joinedload
from pydantic import BaseModel
from fastapi_cache.decorator import cache

from .base import BaseRepository
from src.repositories.utils import booked_cottage
from src.models.cottage import CottageModel
from src.repositories.mappers.mappers import CottageMapper

class CottageRepository(BaseRepository):
    model = CottageModel
    mapper = CottageMapper

    
    async def get_free_cottage(self,id_org : int, data : BaseModel, pag : BaseModel ):
        query = await booked_cottage(id_org, data, pag)
        result = await self.session.execute(query)
        result = result.scalars().all()
        return await self.get_filtered(CottageModel.id.in_(result))
    
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).options(joinedload(self.model.facilities)).filter_by(**filter_by)
        result = await self.session.execute(query)
        if result == None:
            return {"message" : "Объект не найден"}
        model = result.unique().scalars().one_or_none()
        return self.mapper.map_to_domain(model)
    
   
