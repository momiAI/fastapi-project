from sqlalchemy import select,insert,values




class BaseRepository:
    model = None

    def __init__(self,session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    
    async def insert_to_database(self,insert_data):
        stmt = insert(self.model).values(**insert_data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.fetchone()[0]