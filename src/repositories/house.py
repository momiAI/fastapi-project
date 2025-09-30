from .base import BaseRepository
from src.models.house import HouseModel
from sqlalchemy import select

class HouseRepository(BaseRepository):
    model = HouseModel

    async def get_selection(self,data_selection):
        query = select(self.model)
        print(data_selection)
        if data_selection.get("city"):
            query = query.filter(self.model.city.ilike(f"%{data_selection.get('city')}%"))
        if data_selection.get("title"):
            query = query.filter(self.model.title.ilike(f"%{data_selection.get('title')}%"))

        query = query.limit(data_selection.get("per_page")).offset(data_selection.get("per_page") * (data_selection.get("page") - 1))
        result = await self.session.execute(query)

        return result.scalars().all()

