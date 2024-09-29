from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import async_session_maker


async def get_async_database() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


DatabaseDependencies = Annotated[AsyncSession, Depends(get_async_database)]
