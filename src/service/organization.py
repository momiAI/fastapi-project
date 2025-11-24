

from src.route.dependency import SerchNotBook, UserIdDep
from src.schemas.organization import OrganizationAdd, OrganizationToDateBase, OrganizationUpdate
from src.service.base import BaseService

class OrganizationService(BaseService):
    
    async def not_booked(self,data: SerchNotBook):
        return await self.db.organization.get_free_organization_by_cottage(data)
      
    
    async def add_organization(
        self,
        user_id: UserIdDep,
        data: OrganizationAdd):
        
        update_data = OrganizationToDateBase(user_id=user_id, **data.model_dump())
        result =  await self.db.organization.insert_to_database(update_data)
        await self.db.commit()
        return result
        
    async def delete_organization(self,id):
        result = await self.db.organization.delete_by_id(id)
        await self.db.commit()
        return result
        
    async def update_organization(
        self,
        id: int,
        data: OrganizationUpdate
    ):
        result = await self.db.organization.patch_object(id, data)
        await self.db.commit()
        return result
        