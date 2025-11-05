import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from .config import settings
from sqlalchemy import text,NullPool
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(settings.db_url)
engine_null_pool = create_async_engine(settings.db_url,poolclass = NullPool)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False) 
async_session_maker_null_pool = async_session_maker(bind=engine_null_pool, expire_on_commit = False)


class Base(DeclarativeBase):
    pass