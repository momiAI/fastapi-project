from src.service.base import BaseService
from src.route.dependency import HomeSelection
from src.schemas.house import HomeAdd,HomePATCH

class HouseService(BaseService):

    async def get_house(self,id : int):
        return await self.db.house.get_by_id(id)
    
    async def get_selection_homes(self,home_data: HomeSelection):
        return await self.db.house.get_selection(home_data)
    
    async def get_homes(self):
        return await self.db.house.get_all()
    
    async def delete_home(self,id_house : int ):
        return await self.db.house.delete_by_id(id_house)
    
    async def post_home(self,home_data: HomeAdd):
        return await self.db.house.insert_to_database(home_data)
    
    async def put_home(self,home_search: HomePATCH,home_data: HomeAdd):
        return await self.db.house.edit_full(home_data, home_search)
    
    async def patch_home(self,home_id: int,home_data: HomePATCH):
        return await self.db.house.patch_object(home_id, home_data)