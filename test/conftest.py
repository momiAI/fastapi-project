# ruff: noqa: E402
import asyncio
import pytest
import json
from httpx import ASGITransport, AsyncClient
from datetime import date
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.models import *  # noqa: F403
from src.main import app
from src.config import settings
from src.utis.db_manager import DbManager
from src.database import Base, engine, async_session_maker_null_pool
from src.schemas.users import UserAdd
from src.schemas.organization import OrganizationToDateBase
from src.schemas.cottage import CottageAdd, CottageToDateBase
from src.schemas.facilities import AsociationFacilitiesCottage, FacilitiesCottageAdd
from src.schemas.booking import Booking
from src.utis.createsuperuser import create_super_user
from src.config import settings

@pytest.fixture(scope="function", autouse=True)
async def db():
    async with DbManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="module")
async def db_():
    async with DbManager(session_factory=async_session_maker_null_pool) as db_:
        yield db_


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_data(async_main, ac):
    async def jsoan_load(src: str):
        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    [
        await ac.post("/house/add", json=j)
        for j in await jsoan_load(r"test\json\house.json")
    ]


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(ac):
    data = UserAdd(
        email="test111@example.ru",
        password="password",
        last_name="User",
        first_name="Last",
        phone_number="+7321457691",
    )
    response = await ac.post("/auth/register", json=data.model_dump())
    res = response.json()
    assert res["message"] == "OK"


@pytest.fixture(scope="function",autouse=False)
async def test_register_superuser():
    await create_super_user()


@pytest.fixture(scope="function",autouse=False)
async def test_login_superuser(ac,test_register_superuser):
    response = await ac.post(
        "/auth/login", json={"email": settings.ADMIN_EMAIL, "password": settings.ADMIN_PASSWORD}
    )
    res = response.json()
    assert response.status_code == 200
    assert "access_token" in res
    yield ac

@pytest.fixture(scope="session", autouse=True)
async def test_auth_user_ac(ac, test_register_user):
    response = await ac.post(
        "/auth/login", json={"email": "test111@example.ru", "password": "password"}
    )
    res = response.json()
    assert response.status_code == 200
    assert "access_token" in res
    yield ac


@pytest.fixture(scope="module", autouse=True)
async def test_add_organizaion(test_register_user, db_):
    user_id = (await db_.user.get_all())[0].id
    data = OrganizationToDateBase(
        user_id=user_id,
        name="Дворянская поляна",
        description="Очень большое описание",
        city="Донецк",
        location="48.0000 37.0000",
    )

    await db_.organization.insert_to_database(data)
    await db_.commit()


@pytest.fixture(scope="module", autouse=True)
async def test_add_facilitie_cottage(db_):
    data = ["Барбекю", "Гриль", "Лес", "Ставок", "Рыбалка", "Горы"]

    [
        await db_.facilcott.insert_to_database(FacilitiesCottageAdd(title=f))
        for f in data
    ]
    await db_.commit()


@pytest.fixture(scope="module", autouse=True)
async def test_add_cottage(test_add_organizaion, db_, test_add_facilitie_cottage):
    id_org = (await db_.organization.get_all())[0].id
    data = CottageAdd(
        name_house="Барский дом",
        description="Огромный дом у речки на 8 человек",
        people=8,
        price=6000,
        animals=True,
        facilities_ids=[1, 2, 3],
    )
    data_update = CottageToDateBase(organization_id=id_org, **data.model_dump())
    cottage = await db_.cottage.insert_to_database(data_update)
    await db_.asociatfacilcott.insert_to_database_bulk(
        [
            AsociationFacilitiesCottage(id_cottage=cottage.id, id_facilities=i)
            for i in data.facilities_ids
        ]
    )
    await db_.commit()


@pytest.fixture(scope="module", autouse=True)
async def test_book_cottage(db_, test_add_cottage, test_register_user):
    cottage_id = (await db_.cottage.get_all())[0].id
    user_id = (await db_.user.get_all())[0].id

    data = Booking(
        cottage_id=cottage_id,
        user_id=user_id,
        date_start=date(2025, 11, 11),
        date_end=date(2025, 11, 12),
        price=6000,
    )

    await db_.booking.insert_to_database(data)
    await db_.commit()
