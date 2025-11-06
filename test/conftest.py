import pytest
import json
from httpx import ASGITransport, AsyncClient

from src.models import *
from src.main import app
from src.config import settings
from src.utis.db_manager import DbManager
from src.database import Base,engine_null_pool
from src.database import async_session_maker_null_pool


@pytest.fixture(scope='function',autouse=True)
async def db():
    async with DbManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:    
        yield ac


@pytest.fixture(scope = "session",autouse=True)
async def async_main():
    assert settings.MODE == "TEST"


    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



    
@pytest.fixture(scope="session", autouse= True)
async def add_data(async_main,ac):


    async def jsoan_load(src : str):
        with open(src,'r',encoding="utf-8") as f:
            data = json.load(f)
        return data 


    [await ac.post("/auth/register", json=j) for j in await jsoan_load(r"test\json\user.json")]
    [await ac.post("/house/add", json = j) for j in await jsoan_load(r'test\json\house.json')]