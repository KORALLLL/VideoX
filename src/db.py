from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.config import cfg

async_engine = create_async_engine(
    cfg.database.async_database_url,
)
async_session_maker = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)

Base = declarative_base()


async def create_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
