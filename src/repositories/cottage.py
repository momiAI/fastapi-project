from pydantic import BaseModel
from .base import BaseRepository
from src.repositories.utils import booked_cottage
from src.models.cottage import CottageModel
from src.schemas.cottage import Cottage


class CottageRepository(BaseRepository):
    model = CottageModel
    schema = Cottage

    async def get_free_cottage(self,id_org : int, data : BaseModel, pag : BaseModel ):
        query = await booked_cottage(id_org, data, pag)
        result = await self.session.execute(query)
        result = result.scalars().all()
        return await self.get_filtered(CottageModel.id.in_(result))