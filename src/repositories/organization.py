from pydantic import BaseModel
from sqlalchemy import select
from .base import BaseRepository
from src.repositories.utils import booked_cottage,booked_organization
from src.schemas.organization import Organization
from src.models.organization import OrganizationModel

class OrganizationRepository(BaseRepository):
    model = OrganizationModel
    schema = Organization

    async def get_access_user_by_org(self,id_user : int, id_org : int):
        query = select(self.model).where(self.model.id == id_org and self.model.user_id)
        result = await self.session.execute(query)
        model = result.first()
        if model:
            return True
        else: 
            return False
        
    async def get_free_organization_by_cottage(self, data : BaseModel ):
        query = await booked_organization(data)
        result = await self.session.execute(query)
        result = result.scalars().all()
        return await self.get_filtered(OrganizationModel.id.in_(result)) 