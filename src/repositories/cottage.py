from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel


from .base import BaseRepository
from src.repositories.utils import free_cottage
from src.models.cottage import CottageModel
from src.repositories.mappers.mappers import CottageMapper
from src.utis.exception import ObjectNotFound


class CottageRepository(BaseRepository):
    model = CottageModel
    mapper = CottageMapper

    async def get_free_cottage(self, id_org: int, data: BaseModel, pag: BaseModel):
        query = await free_cottage(id_org, data, pag)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )
        try:
            result = await self.session.execute(query)
        except DBAPIError:
            raise ObjectNotFound
        
        model = result.unique().scalars().one_or_none()
        if model is None:
            return {"message": "Объект не найден"}
        return self.mapper.map_to_domain(model)
