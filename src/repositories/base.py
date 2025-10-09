from sqlalchemy import select,insert,values,update,or_,delete
from pydantic import BaseModel
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

class BaseRepository:
    model = None
    schema : BaseModel = None


    def __init__(self,session):
        self.session = session


    async def searching(self,filter_by : BaseModel):
        conditions = [getattr(self.model,key) == value for key,value in filter_by.items() if value is not None]
        query = select(self.model).filter(*conditions)
        search = await self.session.execute(query)
        return search.scalars().one_or_none()


    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model,from_attributes=True) for model in result.scalars().all()]
    
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        if result == None:
            return {"message" : "Объект не найден"}
        model = result.scalars().one_or_none()
        return self.schema.model_validate(model, from_attributes= True)

    async def insert_to_database(self,insert_data  : BaseModel):
        stmt = insert(self.model).values(**insert_data).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.fetchone()[0]
        return [self.schema.model_validate(model, from_attributes=True)]
    

    async def edit_full(self, edit_data : BaseModel, filter_by : BaseModel):
        objectModel = await self.searching(filter_by)
        if objectModel == None:
            return {"message" : "Item not found"}
        else:
            stmt = update(self.model).where(self.model.id == objectModel.id).values(**edit_data).returning(self.model)
            result = await self.session.execute(stmt)
            model = result.fetchone()[0]
            return [self.schema.model_validate(model, from_attributes=True)]

    
    async def delete_by_id(self, id : int):
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            return (self.schema.model_validate(result.scalars().one(),from_attributes=True))
        except NoResultFound:
            return HTTPException(status_code=401, detail="Объект не найден")


    async def delete(self,filter_by : BaseModel):
        objectModel = await self.searching(filter_by)
        if objectModel == None:
            return {"message" : "Item not found"}
        else: 
            stmt = delete(self.model).where(self.model.id == objectModel.id).returning(self.model)
            result = await self.session.execute(stmt)
            model =  result.fetchone()[0]
            return [self.schema.model_validate(model, from_attributes=True)]
       
        
    async def get_by_id(self, id : int):
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return [self.schema.model_validate(model, from_attributes=True)]

    

    async def patch_object(self, id : int , data_patch : BaseModel):
        stmt = update(self.model).where(self.model.id == id).values(**data_patch).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one_or_none() 
        return [self.schema.model_validate(model, from_attributes=True)]