from sqlalchemy import select
from .base import BaseRepository
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