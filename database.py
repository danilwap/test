from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine, Table
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

PG_DATABASE="postgres"
PG_HOST="45.146.164.180"
PG_PASS="12345678"
PG_PORT=5432
PG_USER="postgres"

URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
engine = create_async_engine(URL)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


#----------------------------------- Module CRUD ------------------------------------------

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_data(query):
    async with get_db() as db:
        try:
            result = await db.execute(query)
            return result
        except Exception as ex:
            return f"Произошла ошибка {ex}"

async def insert_data(query):
    async with get_db() as db:
        try:
            await db.execute(query)
            await db.commit()
            return 'Новая запись добавлена'
        except Exception as ex:
            return f"Произошла ошибка {ex}"
