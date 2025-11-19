from pydantic import BaseModel
from .base import BaseRepository
from src.models.house import HouseModel
from sqlalchemy import select
from src.repositories.mappers.mappers import HouseMapper


class HouseRepository(BaseRepository):
    model = HouseModel
    mapper = HouseMapper

    async def get_selection(self, data_selection : BaseModel):
        per_page = 5 or data_selection.per_page
        query = select(self.model)
        if data_selection.city:
            query = query.filter(
                self.model.city.ilike(data_selection.city)
            )
        if data_selection.title:
            query = query.filter(
                self.model.title.ilike(data_selection.title)
            )

        query = query.limit(per_page).offset(
            per_page * (data_selection.page - 1)
        )
        result = await self.session.execute(query)

        models = result.scalars().all()
        return [self.mapper.map_to_domain(model) for model in models]
