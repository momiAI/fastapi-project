from sqlalchemy import select,insert,values,update,or_
from pydantic import BaseModel



class BaseRepository:
    model = None

    def __init__(self,session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    
    async def insert_to_database(self,insert_data  : BaseModel):
        stmt = insert(self.model).values(**insert_data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.fetchone()[0]
    # Дописать эту фунцкию пока при запросе передаёт WHERE houses.title = 'Донецк' AND houses.city = 'string и т.д 
    #Есть какой то or_ нужно разобраться !
    async def edit_full(self, edit_data : BaseModel, filter_by : BaseModel):
        stmt = select(self.model).filter(or_(**filter_by))
        print(stmt.compile(compile_kwargs ={"literal_binds" : True}))
        search = await self.session.execute(stmt)

        return search.scalars().all()
        #stmt = update(self.model).where(**filter_by.model_dump()).values(**edit_data).returning(self.model)
        #result = await self.session.execute(stmt)
        #return result.scalars().one()