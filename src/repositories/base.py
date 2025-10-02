from sqlalchemy import select,insert,values,update,or_,delete
from pydantic import BaseModel



class BaseRepository:
    model = None

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
        return result.scalars().all()
    
    
    async def insert_to_database(self,insert_data  : BaseModel):
        stmt = insert(self.model).values(**insert_data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.fetchone()[0]
    

    async def edit_full(self, edit_data : BaseModel, filter_by : BaseModel):
        objectModel = await self.searching(filter_by)
        if objectModel == None:
            return {"message" : "Item not found"}
        else:
            stmt = update(self.model).where(self.model.id == objectModel.id).values(**edit_data).returning(self.model)
            result = await self.session.execute(stmt)
            return result.fetchone()[0]

    
    async def delete(self,filter_by : BaseModel):
        objectModel = await self.searching(filter_by)
        if objectModel == None:
            return {"message" : "Item not found"}
        else: 
            stmt = delete(self.model).where(self.model.id == objectModel.id).returning(self.model)
            result = await self.session.execute(stmt)
            return result.fetchone()[0]
       
        
