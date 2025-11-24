from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError,NoResultFound,DBAPIError
from pydantic import BaseModel
from fastapi import HTTPException
from src.repositories.mappers.base import DataMapper
from src.utis.exception import IncorrectData,ObjectNotFound,IncorrectDataCottage

class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def searching(self, filter_by: BaseModel):
        conditions = [
            getattr(self.model, key) == value
            for key, value in filter_by.items()
            if value is not None
        ]
        query = select(self.model).filter(*conditions)
        search = await self.session.execute(query)
        return search.scalars().one_or_none()

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain(model) for model in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain(model)
    
    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFound
        return self.mapper.map_to_domain(model)

    async def insert_to_database(self, insert_data: BaseModel):
        stmt = (
            insert(self.model).values(**insert_data.model_dump()).returning(self.model)
        )
        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise IncorrectData
        except DBAPIError:
            raise IncorrectDataCottage
        model = result.unique().scalars().one()
        return self.mapper.map_to_domain(model)


    async def insert_to_database_bulk(self, insert_data: list[int]):
        stmt = insert(self.model).values([i.model_dump() for i in insert_data])
        try:
            await self.session.execute(stmt)
        except IntegrityError:
                    raise IncorrectData
        

    async def edit_full(self, edit_data: BaseModel, filter_by: BaseModel):
        objectModel = await self.searching(filter_by)
        if objectModel is None:
            return {"message": "Item not found"}
        else:
            stmt = (
                update(self.model)
                .where(self.model.id == objectModel.id)
                .values(**edit_data.model_dump(exclude_unset=True))
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            model = result.fetchone()[0]
            return self.mapper.map_to_domain(model)

    async def get_filtered(self, *filte, **filter_by):
        query = select(self.model).filter(*filte).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain(model) for model in result.scalars().all()]

    async def delete_by_id(self, id: int):
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            return self.mapper.map_to_domain(result.scalars().one())
        except NoResultFound:
            return HTTPException(status_code=404, detail="Объект не найден")

    async def delete(self, filter_by: BaseModel):
        objectModel = await self.searching(filter_by.model_dump(exclude_unset=True))
        if objectModel is None:
            return {"message": "Item not found"}
        else:
            stmt = (
                delete(self.model)
                .where(self.model.id == objectModel.id)
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            model = result.fetchone()[0]
            return self.mapper.map_to_domain(model)

    async def get_by_id(self, id: int):
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFound
        return self.mapper.map_to_domain(model)

    async def get_all_by_filter(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain(model) for model in result.scalars().all()]

    async def patch_object(self, id: int, data_patch: BaseModel):
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(data_patch.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        try:
            result = await self.session.execute(stmt)
        except DBAPIError:
            raise IncorrectDataCottage
        try:
            model = result.scalar_one()
        except NoResultFound: 
            raise ObjectNotFound
        return self.mapper.map_to_domain(model)
