from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

# expire_on_commit=False — щоб об'єкти залишались доступними після commit без повторного запиту
sessionmaker = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Залежність FastAPI для ін'єкції сесії БД у маршрути
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session
