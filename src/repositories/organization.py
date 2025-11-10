from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from fastapi_cache.decorator import cache

from .base import BaseRepository
from src.repositories.utils import booked_cottage,booked_organization
from src.schemas.organization import Organization
from src.models.organization import OrganizationModel
from src.repositories.mappers.mappers import OrganizationMapper

class OrganizationRepository(BaseRepository):
    model = OrganizationModel
    mapper = OrganizationMapper


    #@cache
    async def get_access_user_by_org(self,id_user : int, id_org : int):
        
        query = select(self.model).where(self.model.id == id_org , self.model.user_id == id_user)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
            print(model.id)
        except NoResultFound:
            return False
        if model:
            return True
        
    async def get_free_organization_by_cottage(self, data : BaseModel ):
        query = await booked_organization(data)
        result = await self.session.execute(query)
        result = result.scalars().all()
        return await self.get_filtered(OrganizationModel.id.in_(result)) 