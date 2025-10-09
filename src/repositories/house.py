from .base import BaseRepository
from src.models.house import HouseModel
from src.schemas.house import House
from sqlalchemy import select

class HouseRepository(BaseRepository):
    model = HouseModel
    schema = House


    async def get_selection(self,data_selection):
        query = select(self.model)
        if data_selection.get("city"):
            query = query.filter(self.model.city.ilike(f"%{data_selection.get('city')}%"))
        if data_selection.get("title"):
            query = query.filter(self.model.title.ilike(f"%{data_selection.get('title')}%"))

        query = query.limit(data_selection.get("per_page")).offset(data_selection.get("per_page") * (data_selection.get("page") - 1))
        result = await self.session.execute(query)

        models = result.scalars().all()
        return [self.schema.model_validate(model,from_attributes=True) for model in models]

