import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

POSTGRES_URL = config.POSTGRES_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    POSTGRES_URL, pool_size=config.POSTGRES_MAX_POOL_SIZE, future=True
)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
