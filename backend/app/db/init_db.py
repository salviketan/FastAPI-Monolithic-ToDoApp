from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal


async def init_db(db: AsyncSession) -> None:
    pass


async def run_init_db() -> None:
    async with AsyncSessionLocal() as session:
        await init_db(db=session)
