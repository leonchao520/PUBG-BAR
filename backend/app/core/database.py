from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings

engine = None
async_session = None

if not settings.dev_mode and settings.database_url:
    engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    """FastAPI dependency: get a database session. In dev mode, yield None."""
    if async_session is None:
        yield None
        return
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables on startup. No-op in dev mode."""
    if engine:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
