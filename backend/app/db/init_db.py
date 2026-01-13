from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from .session import engine


async def init_db():
    '''Создание всех таблиц, если их нет'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)