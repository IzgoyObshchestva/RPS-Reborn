from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from ..core.config import settings
from typing import AsyncGenerator

engine = create_async_engine(url=settings.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session