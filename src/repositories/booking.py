from fastapi_cache.decorator import cache
from pydantic import BaseModel
from sqlalchemy import select,insert,values,update,or_,delete,func

from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.models.cottage import CottageModel 
from src.repositories.utils import booked_cottage
from src.repositories.mappers.mappers import BookingMapper


 
class BookingRepository(BaseRepository):
    model = BookingModel
    mapper = BookingMapper

   
    async def free_cottage(self, id_org : int, data : BaseModel, pag : BaseModel ):
        query = await booked_cottage(id_org, data, pag)
        return await self.get_filtered(BookingModel.cottage_id.in_(query))
    
    