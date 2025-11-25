from src.route.dependency import SuperUserDep
from src.schemas.facilities import FacilitiesCottageAdd
from src.service.base import BaseService

class FacilitiesService(BaseService):
    
    async def get_all_facilitiec_cottage(self):
        return await self.db.facilcott.get_all()

    async def add_facilitiec_cottage(
        self,
        data: FacilitiesCottageAdd
    ):
        result = await self.db.facilcott.insert_to_database(data)
        await self.db.commit()
        return result
