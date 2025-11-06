import pytest
import json
from httpx import ASGITransport, AsyncClient
from src.main import app
from src.config import settings
from src.database import Base,engine_null_pool
from src.models import *



@pytest.fixture(scope = "session",autouse=True)
async def async_main():
    assert settings.MODE == "TEST"


    async with engine_null_pool.begin() as db:
        await db.run_sync(Base.metadata.drop_all)
        await db.run_sync(Base.metadata.create_all)



    
@pytest.fixture(scope="session", autouse= True)
async def add_data(async_main):


    async def jsoan_load(src : str):
        with open(src,'r',encoding="utf-8") as f:
            data = json.load(f)
        return data 


    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:    
        [await ac.post("/auth/register", json=j) for j in await jsoan_load(r"test\json\user.json")]
        [await ac.post("/house/add", json = j) for j in await jsoan_load(r'test\json\house.json')]