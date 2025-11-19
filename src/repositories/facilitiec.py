from sqlalchemy import select, delete, insert
from sqlalchemy.exc import IntegrityError

from src.repositories.base import BaseRepository
from src.models.facilitiec import (
    FacilitiesCottageModel,
    AsociationFacilitiesCottageModel,
)
from src.repositories.mappers.mappers import (
    FacilitiesCottageMapper,
    AsociationFacilitiesCottageMapper,
)
from src.utis.exception import ObjectNotFound


class FacilitiesCottageRepository(BaseRepository):
    model = FacilitiesCottageModel
    mapper = FacilitiesCottageMapper


class AsociationFacilitiesCottageRepository(BaseRepository):
    model = AsociationFacilitiesCottageModel
    mapper = AsociationFacilitiesCottageMapper

    async def patch_facilities(self, id_cottage, data: list[int]):
        query_fac = await self.session.execute(
            select(self.model.id_facilities).where(self.model.id_cottage == id_cottage)
        )
        facilitiec_ids = query_fac.scalars().all()
        add_facilities = set(data) - set(facilitiec_ids)
        if add_facilities != set():
            add_dict = [
                {"id_cottage": id_cottage, "id_facilities": i} for i in add_facilities
            ]
            stmt_delete = delete(self.model).where(
                self.model.id_cottage == id_cottage, self.model.id_facilities.in_(data)
            )
            stmt_inser = insert(self.model).values(add_dict)
            await self.session.execute(stmt_delete) 
            try:
                await self.session.execute(stmt_inser)
            except IntegrityError:
                raise ObjectNotFound
        else:
            stmt_delete = delete(self.model).where(
                self.model.id_cottage == id_cottage, self.model.id_facilities.in_(data)
            )
            await self.session.execute(stmt_delete)             

